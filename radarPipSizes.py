import logging
import math
import os
import pickle
import pprint
import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from scripts import filenameToTitle
from scripts.data import getPipSize

if TYPE_CHECKING:
    from matplotlib.axes import Axes

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
load_dotenv()


@dataclass
class PlotData:
    """Plot data cache"""

    pipSizes: dict[str, Decimal]


PLOT_DATA: PlotData | None = None
CACHE_FILE = Path("./caches/radarPipSizes.pickle")

if CACHE_FILE.exists():
    logging.info("Loading previous cache from %s", CACHE_FILE)
    logging.info(
        "If the game extract files have been updated, delete that cache and rerun this script."
    )
    with open(CACHE_FILE, "rb") as f:
        PLOT_DATA = pickle.load(f)
else:
    logging.info("No cache found, loading from game extractions...")

    GAME_EXTRACT_ROOT = os.environ.get("GAME_EXTRACT_ROOT")

    if GAME_EXTRACT_ROOT is None:
        logging.critical("GAME_EXTRACT_ROOT not set, exitting")
        sys.exit(1)

    PREFAB_ROOT = (
        Path(GAME_EXTRACT_ROOT) / "ExportedProject" / "Assets" / "PrefabInstance"
    )

    IGNORE_LIST = [
        "MaskedPlayerEnemy",
        "Player",
        "PlayerRagdoll",
        "PlayerRagdollBurnt Variant",
        "PlayerRagdollElectrocuted Variant",
        "PlayerRagdollHeadBurst Variant",
        "PlayerRagdollSpring Variant",
        "PlayerRagdollWithComedyMask Variant",
        "PlayerRagdollWithTragedyMask Variant",
        "RadMechNestSpawnObject",
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
        pipSizes[path.stem] = getPipSize(path)
    PLOT_DATA = PlotData(pipSizes)

    logging.info("Generating caches...")
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(PLOT_DATA, f)


assert PLOT_DATA is not None

logging.info("Breif report of loaded data: %s", pprint.pformat(PLOT_DATA.pipSizes))
logging.info("Plotting...")


BASE_IMG = plt.imread("./assets/RadarPipSizeBase.png")
BACKGROUND_COLOR = "black"
TEXT_COLOR = (0, 0.886, 0.898)
N_COLS = 5
N_ROWS = math.ceil(len(PLOT_DATA.pipSizes) / N_COLS)
fig, axs = plt.subplots(N_ROWS, N_COLS, figsize=(9, 5), dpi=200)

fig.patch.set_facecolor(BACKGROUND_COLOR)
matplotlib.rcParams["text.color"] = TEXT_COLOR
fontPath = Path("./assets/3270-Regular.ttf")

for ax in axs.flatten():
    ax.set_axis_off()
    ax.set_aspect("auto")
    ax.set_facecolor(BACKGROUND_COLOR)

for i, item in enumerate(PLOT_DATA.pipSizes.items()):
    filename, pipSize = item

    currentRow = i // N_COLS
    currentCol = i % N_COLS

    ax: "Axes" = axs[currentRow][currentCol]
    ax.set_title(filenameToTitle(filename), font=fontPath, color=TEXT_COLOR, size=14)

    img = BASE_IMG.copy()

    plotCircleRadius = pipSize * 10

    yLimBottom = min(80, math.ceil(150 - plotCircleRadius)) - 10
    yLimTop = max(230, math.ceil(150 + plotCircleRadius)) + 10
    ax.set_ylim(yLimBottom, yLimTop)
    entityPipCircle = patches.Circle(
        (150, 150), float(plotCircleRadius), color=(1, 0, 0.052129745)
    )

    ax.imshow(img)
    ax.add_patch(entityPipCircle)

fig.tight_layout()
fig.savefig("./outputs/radarPipSizes.png")
