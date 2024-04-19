import logging
import pickle
from dataclasses import dataclass
from pathlib import Path

from scripts.data import PipSize

logger = logging.getLogger(__name__)


CACHE_FILE = Path("./caches/radarPipSizes.pickle")


@dataclass
class PlotCache:
    """Plot data & cache object"""

    pipSizes: dict[str, PipSize]


def write_cache(plotCache: PlotCache):
    logger.info("Writing cache to %s", CACHE_FILE)
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(plotCache, f)


def load_cache() -> PlotCache:
    logger.info("Attempt to load cache from %s", CACHE_FILE)
    with open(CACHE_FILE, "rb") as f:
        return pickle.load(f)
