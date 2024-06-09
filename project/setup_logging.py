import logging


def setup_logging() -> None:
    """
    Configure logger.

    This function sets up the logging configuration for the project.
    It configures the logger to log messages at the INFO level and uses a specific format.

    Args:
        None

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s <%(threadName)s> %(message)s",
    )
