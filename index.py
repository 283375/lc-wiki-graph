# pylint: disable=no-name-in-module, c-extension-no-member

from lxml import etree
from lxml.etree import _Element, _ElementTree

NS_MAP = {"svg": "http://www.w3.org/2000/svg"}

parser = etree.XMLParser(encoding="utf-8")
root = etree.parse("./assets/RadarPipSizeSeparateBase.svg", parser=parser)
assert isinstance(root, _ElementTree)

enemyMapDot = root.xpath(r"//svg:ellipse[@id='path4']", namespaces=NS_MAP)[0]
assert isinstance(enemyMapDot, _Element)


enemyMapDot.attrib["rx"] = "2"
enemyMapDot.attrib["ry"] = "5"

root.write("./output.svg")
