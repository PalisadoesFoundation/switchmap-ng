"""switchmap classes that manage the DB uploading of polled data."""

import os.path
import os
import tempfile

# Import project libraries
from multiprocessing import get_context
from switchmap.core import log
from switchmap.core import files
from switchmap import AGENT_INGESTER, AGENT_POLLER
from switchmap.server.db.table import IZone
from switchmap.server.db.table import IRoot
from switchmap.server.db.table import event as _event
from switchmap.server.db.table import zone as _zone
from switchmap.server.db.table import root as _root
from switchmap.server.db.table import ip as _ip
from switchmap.server.db.table import mac as _mac
from switchmap.server import ZoneData, ZoneDevice, EventObjects
from switchmap.server.db.ingest import update_device
from switchmap.server.db.zone import update_zone


class Ingest:
    """Read cache files in the DB."""

    def __init__(
        self,
        config,
        test=False,
        test_cache_directory=None,
        multiprocessing=False,
    ):
        """Initialize class.

        Args:
            config: ConfigServer object
            test: True if testing
            test_cache_directory: Ingest directory. Only used when testing.
            purge: Purge events if True

        Returns:
            None

        """
        # Initialize key variables
        self._config = config
        self._test = test
        self._test_cache_directory = test_cache_directory
        self._name = "ingest"
        self._multiprocessing = bool(multiprocessing)

    def process(self):
        """Process files in the cache.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        cache_directory = (
            self._config.cache_directory()
            if bool(self._test) is False
            else self._test_cache_directory
        )
        poller_lock_file = files.lock_file(AGENT_POLLER, self._config)
        arguments = []

        # Test for the lock file
        lock_file = files.lock_file(self._name, self._config)
        if os.path.isfile(lock_file) is True:
            log_message = """\
Ingest lock file {} exists. Is an ingest process already running?\
""".format(
                lock_file
            )
            log.log2debug(1054, log_message)
            return

        # Create lock file
        open(lock_file, "a").close()

        # Process files
        with tempfile.TemporaryDirectory(
            dir=self._config.ingest_directory()
        ) as tmpdir:
            # Only run the ingest if there is no poller lock file
            # This helps to prevent ingesting files while polling is
            # still running. This is only effective when the poller
            # and ingester are running on the same machine
            if os.path.isfile(poller_lock_file) is False:
                # Copy files from cache to ingest
                files.move_yaml_files(cache_directory, tmpdir)

                # Parallel process the files
                setup_success = setup(tmpdir, self._config)

                if bool(setup_success) is True:
                    # Populate the arguments
                    arguments = [
                        [item.idx_zone, item.data, item.filepath, item.config]
                        for item in setup_success.zones
                    ]

                    # Process the device independent zone data in the
                    # database first
                    if bool(arguments) is True:
                        success = self.zone(arguments)

                    # Process the device dependent in the database second
                    if bool(success):
                        success = self.device(arguments)

                    # Cleanup
                    self.cleanup(setup_success.event)
            else:
                log_message = (
                    "Poller lock file {} exists. Skipping processing of cache "
                    "files. Is the poller running or did it crash unexpectedly?"
                )
                log.log2info(1038, log_message)

        # Delete lock file
        os.remove(lock_file)

    def zone(self, arguments):
        """Ingest the files' zone data.

        Args:
            arguments: List of arguments for the processing the zone
                [[item.idx_zone, item.data, item.filepath, item.config]]

        Returns:
            success: True if successful

        """
        # Initialize key variables
        success = False
        rows = []

        # Return if necessary
        if bool(arguments) is False:
            return success

        # Get the number of threads to use in the pool
        pool_size = self._config.agent_subprocesses()

        # Process the data files
        if bool(self._test) is False:
            if bool(self._multiprocessing) is False:
                ############################
                # Process files serially
                ############################
                for argument in arguments:
                    rows.append(process_zone(*argument))

            else:
                ############################
                # Process files in parallel
                ############################

                # Create a pool of sub process resources
                with get_context("spawn").Pool(processes=pool_size) as pool:
                    # Create sub processes from the pool
                    rows = pool.starmap(process_zone, arguments)

        else:
            ############################
            # Process files sequentially
            ############################
            for argument in arguments:
                rows.append(process_zone(*argument))

        # Process rows for insertion into the database
        macs = list(set([_.macs for _ in rows]))
        ips = list(set([_.ips for _ in rows]))
        _mac.insert_row(macs)
        _ip.insert_row(ips)

        # Return
        success = True
        return success

    def device(self, arguments):
        """Ingest the files' device data.

        Args:
            arguments: List of arguments for the processing the zone
                [[item.idx_zone, item.data, item.filepath, item.config]]

        Returns:
            success: True if successful

        """
        # Initialize key variables
        success = False

        # Return if necessary
        if bool(arguments) is False:
            return success

        # Get the number of threads to use in the pool
        pool_size = self._config.agent_subprocesses()

        # Process the data files
        if bool(self._test) is False:
            if bool(self._multiprocessing) is False:
                ############################
                # Process files serially
                ############################
                for argument in arguments:
                    process_device(*argument)

            else:
                ############################
                # Process files in parallel
                ############################

                # Create a pool of sub process resources
                with get_context("spawn").Pool(processes=pool_size) as pool:
                    # Create sub processes from the pool
                    pool.starmap(process_device, arguments)

        else:
            ############################
            # Process files sequentially
            ############################
            for argument in arguments:
                process_device(*argument)

        # Return
        success = True
        return success

    def cleanup(self, event):
        """Ingest the files' device data.

        Args:
            zones: List of ZoneDevice objects

        Returns:
            None

        """
        # Cleanup
        if bool(self._test) is False:
            # Only update the DB if the skip file is absent.
            if (
                os.path.isfile(files.skip_file(AGENT_INGESTER, self._config))
                is False
            ):
                # Update the event pointer in the root table
                # We don't do this for testing
                root = _root.idx_exists(1)
                if bool(root):
                    _root.update_row(
                        root.idx_root,
                        IRoot(
                            idx_event=event.idx_event,
                            name=root.name,
                            enabled=1,
                        ),
                    )

            # Purge data if requested
            if bool(self._config.purge_after_ingest()) is True:
                log_message = (
                    "Purging database based on configuration parameters."
                )
                log.log2debug(1058, log_message)
                _event.purge()

        else:
            # Delete all DB records related to the event.
            # This is only done for testing
            _event.delete(event.idx_event)


def process_zone(idx_zone, data, filepath, config):
    """Ingest a single file for device updates.

    Args:
        idx_zone: Zone index to be used for the data
        data: Cache file containing data
        filepath: Cache file filepath that contains the data
        config: Daemon configuration

    Returns:
        rows: ZoneObjects object

    """
    # Do nothing if the skip file exists
    skip_file = files.skip_file(AGENT_INGESTER, config)
    if os.path.isfile(skip_file) is True:
        log_message = """\
Skip file {} found. Aborting ingesting {}. A daemon \
shutdown request was probably requested""".format(
            skip_file, filepath
        )
        log.log2debug(1049, log_message)
        return

    # Process the ingested data
    rows = update_zone.process(data, idx_zone)
    return rows


def process_device(idx_zone, data, filepath, config):
    """Ingest a single file for device updates.

    Args:
        idx_zone: Zone index to be used for the data
        data: Cache file containing data
        filepath: Cache file filepath that contains the data
        config: Daemon configuration

    Returns:
        None

    """
    # Do nothing if the skip file exists
    skip_file = files.skip_file(AGENT_INGESTER, config)
    if os.path.isfile(skip_file) is True:
        log_message = """\
Skip file {} found. Aborting ingesting {}. A daemon \
shutdown request was probably requested""".format(
            skip_file, filepath
        )
        log.log2debug(1049, log_message)
        return

    # Process the ingested data
    update_device.process(data, idx_zone)


def setup(src, config):
    """Ingest the files in parallel.

    Args:
        src: Directory where device YAML files are located

    Returns:
        result: EventObjects object

    """
    # Initialize key variables
    result = None
    _zones = []

    # Create a list of files to process
    filepaths = _filepaths(src)

    # Parallel processing
    if bool(filepaths) is True:
        # Create an event
        event = _event.create()

        # Get the _zone data from each file
        for filepath in filepaths:
            _zone = _get_zone(event, filepath)
            _zones.append(
                ZoneDevice(
                    idx_zone=_zone.idx_zone,
                    data=_zone.data,
                    filepath=filepath,
                    config=config,
                )
            )
        result = EventObjects(event=event, zones=_zones)

    # Return
    return result


def _filepaths(src):
    """Get and _event ID for the next polling cycle.

    Args:
        src: Source directory

    Returns:
        filepaths: List of all yaml files in the directory

    """
    # Initialize key variables
    filepaths = []

    # Process files
    src_files = os.listdir(src)
    for filename in src_files:
        filepath = os.path.join(src, filename)
        if os.path.isfile(filepath) and filepath.lower().endswith(".yaml"):
            filepaths.append(filepath)
    return filepaths


def _get_zone(event, filepath):
    """Create an RZone object from YAML file data.

    Args:
        event: RZone object
        filepath: YAML filepath

    Returns:
        result: ZoneData object

    """
    # Read the yaml file
    data = files.read_yaml_file(filepath)

    # Get the zone information
    name = data["misc"]["zone"]
    exists = _zone.exists(event.idx_event, name)
    if bool(exists) is False:
        _zone.insert_row(
            IZone(
                idx_event=event.idx_event,
                name=name,
                notes=None,
                enabled=1,
            )
        )
        exists = _zone.exists(event.idx_event, name)

    # Return
    result = ZoneData(idx_zone=exists.idx_zone, data=data)
    return result
