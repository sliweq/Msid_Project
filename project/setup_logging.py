import logging


def setup_logging() -> None:
    """Configure logger"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s <%(threadName)s> %(message)s",
    )
