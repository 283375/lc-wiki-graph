import logging
from decimal import Decimal
from pathlib import Path
from typing import NamedTuple

from unityparser import UnityDocument

logger = logging.getLogger(__name__)


class PipSize(NamedTuple):
    x: Decimal
    z: Decimal


def getPipSize(prefabFile: str | Path) -> PipSize | None:
    """
    If the input prefab file contains radar pip size definitions, returns it.
    Otherwise, returns `None`.
    """

    if isinstance(prefabFile, Path):
        filepath = prefabFile
    else:
        filepath = Path(prefabFile)

    logger.info("Reading %s", filepath.name)

    mapDotEntry = None
    mapDotTransform = None
    mapDotTransformFather = None

    prefabDoc = UnityDocument.load_yaml(filepath)

    gameObjectEntries = prefabDoc.filter(
        class_names=("GameObject",), attributes=("m_Name", "m_Layer")
    )

    for entry in gameObjectEntries:
        if entry.m_Layer == "14" and "MapDot" in entry.m_Name:
            mapDotEntry = entry
            break

    if mapDotEntry is None:
        logger.error("MapDot GameObject not found")
        return None

    logger.debug("mapDotEntry: %r", mapDotEntry)

    mapDotEntryComponentFileIds = [
        item.get("component", {}).get("fileID") for item in mapDotEntry.m_Component
    ]

    transformEntries = prefabDoc.filter(class_names=("Transform",))
    for entry in transformEntries:
        if entry.anchor in mapDotEntryComponentFileIds:
            mapDotTransform = entry
            break

    if mapDotTransform is None:
        logger.error("MapDot Transform not found")
        return None

    logger.debug("mapDotTransform: %r", mapDotTransform)

    for entry in transformEntries:
        if entry.anchor == mapDotTransform.m_Father["fileID"]:
            mapDotTransformFather = entry
            break

    if mapDotTransformFather is None:
        logger.error("MapDot Transform father not found")
        return None

    logger.debug("mapDotTransformFather: %r", mapDotTransformFather)

    mapDotTransformScale = mapDotTransform.m_LocalScale
    mapDotTransformFatherScale = mapDotTransformFather.m_LocalScale

    pipSizeX = Decimal(mapDotTransformScale["x"]) * Decimal(
        mapDotTransformFatherScale["x"]
    )
    pipSizeZ = Decimal(mapDotTransformScale["z"]) * Decimal(
        mapDotTransformFatherScale["z"]
    )

    return PipSize(x=pipSizeX, z=pipSizeZ)
