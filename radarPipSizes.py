import logging
import os
import pprint
import sys
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv
from matplotlib import font_manager

from scripts import SORT_LIST
from scripts.data import getPipSize
from scripts.data.index import PipSize
from scripts.plot.radarPipSizes import (
    CACHE_FILE,
    PlotCache,
    generateSeparateIcons,
    load_cache,
    plotSummary,
    write_cache,
)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
load_dotenv()


PLOT_CACHE: PlotCache | None = None

if CACHE_FILE.exists():
    try:
        PLOT_CACHE = load_cache()
    except Exception:  # pylint: disable=broad-exception-caught
        logging.exception("Error loading cache from %s", CACHE_FILE)
        logging.info("HINT: You can try deleting that cache, then rerun this script.")
        sys.exit(1)
else:
    logging.info("No cache found, loading from game extractions...")

    GAME_EXTRACT_ROOT = os.environ.get("GAME_EXTRACT_ROOT")

    if GAME_EXTRACT_ROOT is None:
        logging.critical("GAME_EXTRACT_ROOT not set, exitting")
        sys.exit(1)

    PREFAB_ROOT = Path(GAME_EXTRACT_ROOT) / "ExportedProject" / "Assets" / "GameObject"

    IGNORE_LIST = [
        "Player",
        "PlayerRagdoll",
        "PlayerRagdollBurnt Variant",
        "PlayerRagdollElectrocuted Variant",
        "PlayerRagdollHeadBurst Variant",
        "PlayerRagdollSpring Variant",
        "PlayerRagdollWithComedyMask Variant",
        "PlayerRagdollWithTragedyMask Variant",
        "PlayerRagdollHeadGone Variant",
        "PlayerRagdollSlicedInHalf Variant",
        "TestRoom",
        "RadMechNestSpawnObject",
        "PlayerRagdollFlowers Variant",
        "PlayerRagdollScratched Variant",
    ]

    prefabFilePaths: list[Path] = []

    for path in PREFAB_ROOT.glob("*.prefab"):
        if path.stem in IGNORE_LIST:
            continue

        with open(path, "r", encoding="utf-8") as f:
            fileContent = f.read()
            if "MapDot" in fileContent:
                prefabFilePaths.append(path)

    logging.info("Prefabs found: %r", [path.stem for path in prefabFilePaths])
    logging.info("Loading pip sizes...")

    pipSizes = {}
    for path in prefabFilePaths:
        if path.stem in {"MaskedPlayerEnemy", "CadaverBloomBurstEnemy"}:
            pipSize = PipSize(
                x=Decimal(0.0),
                z=Decimal(0.0),
                shouldRenderPlayer=True,
                playerOffset=Decimal(80),
                playerRotation=180,
            )
        else:
            pipSize = getPipSize(path)

        if pipSize is None:
            logging.warning("Pip size not found for %s", path)
            continue

        if path.stem == "CGrowthsScanNode":
            pipSize = pipSize._replace(shouldRenderPlayer=True)

        pipSizes[path.stem] = pipSize

    # sort dict by keys, use sorted
    pipSizes = dict(sorted(pipSizes.items(), key=lambda kv: SORT_LIST.index(kv[0])))

    PLOT_CACHE = PlotCache(pipSizes)

    logging.info("Writing cache...")
    write_cache(PLOT_CACHE)


assert PLOT_CACHE is not None

logging.info("Breif report of loaded data:\n%s", pprint.pformat(PLOT_CACHE.pipSizes))
logging.info("Plotting...")

OUTPUT_PATH = Path("./outputs")

font_manager.fontManager.addfont("./assets/3270-Regular.ttf")
fig = plotSummary(PLOT_CACHE)
fig.text(
    0.005,
    0.01,
    "v81",
    fontsize="xx-large",
    color=(253 / 255, 90 / 255, 23 / 255),
    fontproperties=font_manager.FontProperties(fname="./assets/3270-Regular.ttf"),
)
fig.savefig(OUTPUT_PATH / "radarPipSizes.png")

logging.info("Generating separate icons")

SEPARATE_ICONS_OUTPUT_PATH = OUTPUT_PATH / "radarPipSizes"
SEPARATE_ICONS_OUTPUT_PATH.mkdir(parents=False, exist_ok=True)

icons = generateSeparateIcons(PLOT_CACHE)

for filename, elementRoot in icons.items():
    with open(SEPARATE_ICONS_OUTPUT_PATH / filename, "wb") as f:
        elementRoot.write(f)
