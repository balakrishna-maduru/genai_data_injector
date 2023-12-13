# logger.py
import logging

class LoggerSetup:
    """
    A class for setting up a logger with a console handler.

    Attributes:
    - logger (logging.Logger): Logger instance.

    Methods:
    - __init__(): Initialize the logger.
    - get_logger(): Get the configured logger instance.
    """

    def __init__(self):
        """
        Initialize the LoggerSetup.
        """
        self.logger = logging.getLogger("VersionBumper")
        self._setup_logger()

    def _setup_logger(self):
        """
        Set up a logger with a console handler.
        """
        self.logger.setLevel(logging.DEBUG)

        # Create console handler and set level to INFO
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add ch to logger
        self.logger.addHandler(ch)

    def get_logger(self):
        """
        Get the configured logger instance.

        Returns:
        - logging.Logger: Configured logger instance.
        """
        return self.logger
