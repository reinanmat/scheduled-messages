import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)
