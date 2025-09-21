"""switchmap classes that manage the DB uploading of polled data."""

import os.path
import os
import tempfile
from operator import attrgetter

# Import project libraries
from multiprocessing import get_context
from switchmap.core import log
from switchmap.core import files
from switchmap import AGENT_INGESTER, AGENT_POLLER
from switchmap.server import IngestArgument
from switchmap.server.db.table import IZone
from switchmap.server.db.table import IRoot
from switchmap.server.db.table import IMacIp
from switchmap.server.db.table import event as _event
from switchmap.server.db.table import zone as _zone
from switchmap.server.db.table import root as _root
from switchmap.server.db.table import ip as _ip
from switchmap.server.db.table import mac as _mac
from switchmap.server.db.table import macip as _macip
from switchmap.server import ZoneData, ZoneDevice, EventObjects
from switchmap.server.db.ingest.update import device as update_device
from switchmap.server.db.ingest.update import zone as update_zone


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
            multiprocessing: True if multiprocessing is enabled

        Returns:
            None

        """
        # Initialize key variables
        self._config = config
        self._test = bool(test)
        self._dns = not bool(test)
        self._test_cache_directory = test_cache_directory
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
        pairmacips = None

        # Process files
        with tempfile.TemporaryDirectory(
            dir=self._config.ingest_directory()
        ) as tmpdir:
            # ASYNC ARCHITECTURE: Allow ingester to run while poller is active
            # Copy files from cache to ingest
            files.move_yaml_files(cache_directory, tmpdir)

            # Parallel process the files
            setup_success = setup(tmpdir, self._config)

            if bool(setup_success) is True:
                # Populate the arguments
                arguments = [
                    [
                        IngestArgument(
                            idx_zone=item.idx_zone,
                            data=item.data,
                            filepath=item.filepath,
                            config=item.config,
                            dns=self._dns,
                        )
                    ]
                    for item in setup_success.zones
                ]

                # Process the device independent zone data in the
                # database first
                if bool(arguments) is True:
                    pairmacips = self.zone(arguments)

                # Process the device dependent in the database second
                if bool(pairmacips):
                    self.device(arguments)

                # Cleanup
                self.cleanup(setup_success.event)

    def zone(self, arguments):
        """Ingest the files' zone data.

        Args:
            arguments: List of Argument objects

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

        # Insert ARP table
        pairmacips = insert_arptable(rows)

        # Return
        success = True
        return pairmacips

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
            event: Name of event

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


def process_zone(argument):
    """Ingest a single file for device updates.

    Args:
        argument: Argument object

    Returns:
        rows: ZoneObjects object

    """
    # Initialize key variables
    (idx_zone, data, filepath, config, dns) = _get_arguments(argument)

    # Do nothing if the skip file exists
    skip_file = files.skip_file(AGENT_INGESTER, config)
    if os.path.isfile(skip_file) is True:
        log_message = f"""\
Skip file {skip_file} found. Aborting ingesting {filepath}. A daemon \
shutdown request was probably requested"""
        log.log2debug(1075, log_message)
        return

    # Process the ingested data
    rows = update_zone.process(data, idx_zone, dns=dns)
    return rows


def process_device(argument):
    """Ingest a single file for device updates.

    Args:
        argument: Argument object

    Returns:
        None

    """
    # Initialize key variables
    (idx_zone, data, filepath, config, dns) = _get_arguments(argument)

    # Do nothing if the skip file exists
    skip_file = files.skip_file(AGENT_INGESTER, config)
    if os.path.isfile(skip_file) is True:
        log_message = f"""\
Skip file {skip_file} found. Aborting ingesting {filepath}. A daemon \
shutdown request was probably requested"""
        log.log2debug(1049, log_message)
        return

    # Process the ingested data
    update_device.process(data, idx_zone, dns=dns)


def setup(src, config):
    """Ingest the files in parallel.

    Args:
        src: Directory where device YAML files are located
        config: Configuration object

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


def insert_arptable(data, test=False):
    """Insert values from ARP tables.

    Args:
        data: List of lists of ZoneObjects, one per device
            OR a single ZoneObjects from testing
        test: Sequentially insert values into the database if True.
            Bulk inserts don't insert data with predictable primary keys.

    Returns:
        pairmacips: List of PairMacIp objects

    """
    # List of lists comprehension to get a list, then remove
    # duplicates with set, then recreate a list
    if isinstance(data, list):
        macs = list(set([_ for row in data for _ in row.macs]))
        ips = list(set([_ for row in data for _ in row.ips]))
        pairmacips = list(set([_ for row in data for _ in row.pairmacips]))
    else:
        macs = data.macs
        ips = data.ips
        pairmacips = data.pairmacips

    # Remove any duplicates
    macs = list(set(macs))
    ips = list(set(ips))
    pairmacips = list(set(pairmacips))

    # Insert MAC addresses for all zones
    log_message = (
        "Updating MAC addresses in the DB for all "
        "zones from ARP and NDP ables."
    )
    log.log2debug(1084, log_message)
    if bool(test) is False:
        _mac.insert_row(macs)
    else:
        for row in sorted(macs, key=attrgetter("mac")):
            _mac.insert_row(row)

    # Insert IP addresses for all zones
    log_message = (
        "Updating IP addresses in the DB for all "
        "zones from ARP and NDP tables."
    )
    log.log2debug(1085, log_message)
    if bool(test) is False:
        _ip.insert_row(ips)
    else:
        for row in sorted(ips, key=attrgetter("address")):
            _ip.insert_row(row)

    # Insert ARP entries for all zones
    log_message = "Updating MAC to IP address mapping in the database."
    log.log2debug(1089, log_message)
    insert_macips(pairmacips, test=test)

    # Return
    return pairmacips


def insert_macips(items, test=False):
    """Update the mac DB table.

    Args:
        items: List of PairMacIp objects
        test: Sequentially insert values into the database if True.
            Bulk inserts don't insert data with predictable primary keys.

    Returns:
        None

    """
    # Initialize key variables
    rows = []

    # Insert shit
    if isinstance(items, list) is False:
        items = [items]

    # Process data
    for item in items:
        # Update the database
        mac_exists = _mac.exists(item.idx_zone, item.mac)
        ip_exists = _ip.exists(item.idx_zone, item.ip)

        # Insert
        if bool(mac_exists) and bool(ip_exists):
            macip_exists = _macip.exists(mac_exists.idx_mac, ip_exists.idx_ip)
            if bool(macip_exists) is False:
                # Create a DB record
                rows.append(
                    IMacIp(
                        idx_ip=ip_exists.idx_ip,
                        idx_mac=mac_exists.idx_mac,
                        enabled=1,
                    )
                )

    # Insert the values
    if bool(test) is False:
        _macip.insert_row(rows)
    else:
        row = sorted(rows, key=attrgetter("idx_mac", "idx_ip"))
        _macip.insert_row(row)


def _filepaths(src):
    """Get and _event ID for the next polling cycle.

    Args:
        src: Source directory

    Returns:
        filepaths: List of all yaml files in the directory

    """
    # Initialize key variables
    filepaths = []

    # Log progress
    log_message = "Reading ingest YAML files."
    log.log2info(1234, log_message)

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
        # Log progress
        log_message = f"""\
Creating database zone '{name}' in preparation for database ingest"""
        log.log2info(1054, log_message)

        # Insert
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


def _get_arguments(argument):
    """Ingest a single file for device updates.

    Args:
        argument: Argument object

    Returns:
        result: A tuple of the values of the argument

    """
    # Initialize key variables
    result = (
        argument.idx_zone,
        argument.data,
        argument.filepath,
        argument.config,
        argument.dns,
    )
    return result
