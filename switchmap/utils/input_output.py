"""Switchmap classes that manage Files."""

# Standard imports
import os
import sys
import time

# Switchmap imports
from switchmap.utils import log


class File(object):
    """Represent a tail command."""

    def __init__(self, tailed_file):
        """Method that instantiates the class.

        Check for file validity, assigns callback function to standard out.

        Args:
            tailed_file - File to be followed.

        """
        self.tailed_file = tailed_file
        self.check_file_validity()
        self.tailed_file = tailed_file

    def tail(self, seconds=1, max_lines=50):
        """Do a tail follow.

        If a callback function is registered it is called with every new line,
        else printed to standard out.

        Args:
            seconds: Seconds to wait between each iteration. Default 1.
            max_lines: maximum number of lines to show at start of tail

        """
        # Read file
        with open(self.tailed_file, "r") as file_:
            # Go to EOF and get file size
            file_.seek(0, 2)
            fsize = file_.tell()

            # Get position of last 10K characters, then read to the end
            file_.seek(max(fsize - 10000, 0), 0)
            lines = file_.readlines()  # Read to end

        # Print last max_lines number of lines
        lines = lines[-max_lines:]
        for line in lines:
            print(line.strip())

        # Process file
        with open(self.tailed_file) as file_:
            # Go to the end of file
            file_.seek(0, 2)
            while True:
                # Tail file. Exit if CTRL-C is pressed
                try:
                    # Get the byte offset of the most recent file read op
                    # In other words get current size of file
                    curr_position = file_.tell()

                    # Read line
                    line = file_.readline().strip()

                    # If nothing new, then sleep
                    if not line:
                        # Go to the current end of file
                        file_.seek(curr_position)
                        time.sleep(seconds)
                    else:
                        print(line)
                except KeyboardInterrupt:
                    sys.exit(0)

    def check_file_validity(self):
        """Check whether the a given file exists, is readable and is a file.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        file_ = self.tailed_file

        # Check if exists
        if os.path.exists(file_) is False:
            log_message = "File {} does not exist.".format(file_)
            log.log2die(1018, log_message)

        # Check if file
        if os.path.isfile(file_) is False:
            log_message = "{} is not a file.".format(file_)
            log.log2die(1035, log_message)

        # Check if readable
        if not os.access(file_, os.R_OK):
            log_message = "File {} is not readable.".format(file_)
            log.log2die(1036, log_message)
