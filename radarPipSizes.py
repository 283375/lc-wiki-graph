import logging
import math
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from scripts.getPipSize import getPipSize

if TYPE_CHECKING:
    from matplotlib.axes import Axes

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
load_dotenv()

GAME_EXTRACT_ROOT = os.environ.get("GAME_EXTRACT_ROOT")

if GAME_EXTRACT_ROOT is None:
    logging.critical("GAME_EXTRACT_ROOT not set, exitting")
    sys.exit(1)

PREFAB_ROOT = Path(GAME_EXTRACT_ROOT) / "ExportedProject" / "Assets" / "PrefabInstance"

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

    with open(path, encoding="utf-8") as f:
        fileContent = f.read()
        if "MapDot" in fileContent:
            prefabFilePaths.append(path)

logging.info("Prefabs found: %r", [path.stem for path in prefabFilePaths])

logging.info("Plotting...")

TITLE_MAPPING = {
    "BaboonHawkEnemy": "Baboon Hawk",
    "Blob": "Hygrodere",
    "ButlerEnemy": "Butler",
    "Centipede": "Snare Flea",
    "Crawler": "Thumper",
    "DoublewingedBird": "Manticoil",
    "Flowerman": "Bracken",
    "FlowerSnakeEnemy": "Tulip Snake",
    "ForestGiant": "Forest Keeper",
    "HoarderBug": "Hoarding Bug",
    "JesterEnemy": "Jester",
    "LassoMan": "Lasso Man",
    "MouthDog": "Eyeless Dog",
    "NutcrackerEnemy": "Nutcracker",
    "PufferEnemy": "Spore Lizard",
    "RadMechEnemy": "Old Bird",
    "SandSpider": "Bunker Spider",
    "SandWorm": "Earth Leviathan",
    "SpringMan": "Coil-Head",
}

BASE_IMG = plt.imread("./assets/RadarPipSizeBase.png")
BACKGROUND_COLOR = "black"
TEXT_COLOR = (0, 0.886, 0.898)
N_COLS = 5
N_ROWS = math.ceil(len(prefabFilePaths) / N_COLS)
fig, axs = plt.subplots(N_ROWS, N_COLS, figsize=(9, 5), dpi=200)

fig.patch.set_facecolor(BACKGROUND_COLOR)
matplotlib.rcParams["text.color"] = TEXT_COLOR
fontPath = Path("./assets/3270-Regular.ttf")

for ax in axs.flatten():
    ax.set_axis_off()
    ax.set_aspect("auto")
    ax.set_facecolor(BACKGROUND_COLOR)

for i, path in enumerate(prefabFilePaths):
    currentRow = i // N_COLS
    currentCol = i % N_COLS

    ax: "Axes" = axs[currentRow][currentCol]
    ax.set_title(
        TITLE_MAPPING.get(path.stem, f"!! {path.stem} !!"),
        font=fontPath,
        color=TEXT_COLOR,
        size=14,
    )

    img = BASE_IMG.copy()

    entityPipSize = getPipSize(path)
    assert entityPipSize is not None
    plotCircleRadius = entityPipSize * 10

    yLimBottom = min(80, math.ceil(150 - plotCircleRadius)) - 10
    yLimTop = max(230, math.ceil(150 + plotCircleRadius)) + 10
    ax.set_ylim(yLimBottom, yLimTop)
    entityPipCircle = plt.Circle(
        (150, 150), float(plotCircleRadius), color=(1, 0, 0.052129745)
    )

    ax.imshow(img)
    ax.add_patch(entityPipCircle)

fig.tight_layout()
fig.savefig("./outputs/radarPipSizes.png")
