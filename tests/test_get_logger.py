import logging
import unittest
from genai_inchoate_data.utilities.logger import LoggerSetup

class TestLoggerSetup(unittest.TestCase):

    def setUp(self):
        self.logger_setup = LoggerSetup()

    def test_get_logger(self):
        logger = self.logger_setup.get_logger()

        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "VersionBumper")
        self.assertEqual(logger.level, logging.DEBUG)

        handlers = logger.handlers
        self.assertEqual(len(handlers), 1)

        console_handler = handlers[0]
        self.assertIsInstance(console_handler, logging.StreamHandler)
        self.assertEqual(console_handler.level, logging.INFO)

    def test_logger_messages(self):
        # This test verifies that the logger is able to log messages without errors
        logger = self.logger_setup.get_logger()

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

        # No assertions, just checking for any exceptions during logging

if __name__ == '__main__':
    unittest.main()
