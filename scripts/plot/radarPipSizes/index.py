# pylint: disable=c-extension-no-member

import logging
import math
import pprint
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
from lxml import etree
from lxml.etree import _Element, _ElementTree  # pylint: disable=no-name-in-module
from matplotlib import patches

from scripts import filenameToTitle

from .cache import PlotCache

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def plotSummary(
    plotCache: PlotCache,
    baseImgPath: str | Path = "./assets/RadarPipSizeBase.png",
    fontPath: str | Path = "./assets/3270-Regular.ttf",
) -> "Figure":
    logger.info("Breif report of loaded data: %s", pprint.pformat(plotCache.pipSizes))
    logger.info("Plotting...")

    baseImg = plt.imread(baseImgPath)
    backgroundColor = "black"
    textColor = (0, 0.886, 0.898)
    nCols = 5
    nRows = math.ceil(len(plotCache.pipSizes) / nCols)

    fig, axs = plt.subplots(nRows, nCols, figsize=(9, 5), dpi=200)

    fig.patch.set_facecolor(backgroundColor)
    font = Path(fontPath)

    for ax in axs.flatten():
        ax.set_axis_off()
        ax.set_aspect("auto")
        ax.set_facecolor(backgroundColor)

    for i, item in enumerate(plotCache.pipSizes.items()):
        filename, pipSize = item

        currentRow = i // nCols
        currentCol = i % nCols

        ax: "Axes" = axs[currentRow][currentCol]
        ax.set_title(filenameToTitle(filename), font=font, color=textColor, size=14)

        img = baseImg.copy()

        plotEllipseWidth = pipSize.x * 10 * 2
        plotEllipseHeight = pipSize.z * 10 * 2

        yLimBottom = min(80, math.ceil(150 - plotEllipseHeight / 2)) - 10
        yLimTop = max(230, math.ceil(150 + plotEllipseHeight / 2)) + 10
        ax.set_ylim(yLimBottom, yLimTop)
        entityPipCircle = patches.Ellipse(
            (150, 150),
            width=float(plotEllipseWidth),
            height=float(plotEllipseHeight),
            color=(1, 0, 0.052129745),
        )

        ax.imshow(img)
        ax.add_patch(entityPipCircle)

    fig.tight_layout()
    return fig


def generateSeparateIcons(plotCache: PlotCache) -> dict[str, _ElementTree]:
    namespaceMap = {"svg": "http://www.w3.org/2000/svg"}

    returnDict = {}

    parser = etree.XMLParser(encoding="utf-8")

    for filenameStem, pipSize in plotCache.pipSizes.items():
        root = etree.parse("./assets/RadarPipSizeSeparateBase.svg", parser=parser)
        assert isinstance(root, _ElementTree)

        enemyMapDot = root.xpath(
            r"//svg:ellipse[@id='path4']", namespaces=namespaceMap
        )[0]
        assert isinstance(enemyMapDot, _Element)

        enemyMapDot.attrib["rx"] = str(pipSize.x)
        enemyMapDot.attrib["ry"] = str(pipSize.z)

        stem = f"{filenameToTitle(filenameStem)}"
        stem = stem.replace("!", "_")
        stem = stem.replace(" ", "")
        filename = f"RadarPipSize_{stem}.svg"

        returnDict[filename] = root

    return returnDict
