from . import data

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
    "ClaySurgeon": "Barber",
    "BushWolfEnemy": "Kidnapper Fox",
    "CaveDwellerEnemy": "Maneater",
    "CGrowthsScanNode": "Cadaver Growths",
    "CadaverBloomBurstEnemy": "Cadaver Bloom",
    "GiantKiwi": "Giant Sapsucker",
    "PumaEnemy": "Feiopar",
    "StingrayEnemy": "Backwater Gunkfish",
    "MaskedPlayerEnemy": "Masked",
}

SORT_LIST = [
    "Centipede",  # Snare Flea
    "SpringMan",  # Coil-Head
    "NutcrackerEnemy",  # Nutcracker
    "SandSpider",  # Bunker Spider
    "Blob",  # Hygrodere
    "CaveDwellerEnemy",  # Maneater
    "Flowerman",  # Bracken
    "LassoMan",  # Lasso Man
    "ButlerEnemy",  # Butler
    "MaskedPlayerEnemy",  # Masked
    "HoarderBug",  # Hoarding Bug
    "JesterEnemy",  # Jester
    "StingrayEnemy",  # Backwater Gunkfish
    "CadaverBloomBurstEnemy",  # Cadaver Bloom
    "CGrowthsScanNode",  # Cadaver Growths
    "ClaySurgeon",  # Barber
    "Crawler",  # Thumper
    "PufferEnemy",  # Spore Lizard
    "BaboonHawkEnemy",  # Baboon Hawk
    "ForestGiant",  # Forest Keeper
    "BushWolfEnemy",  # Kidnapper Fox
    "MouthDog",  # Eyeless Dog
    "SandWorm",  # Earth Leviathan
    "PumaEnemy",  # Feiopar
    "RadMechEnemy",  # Old Bird
    "DoublewingedBird",  # Manticoil
    "GiantKiwi",  # Giant Sapsucker
    "FlowerSnakeEnemy",  # Tulip Snake
]


def filenameToTitle(filename: str) -> str:
    title = TITLE_MAPPING.get(filename)
    return title if title is not None else f"!! {filename} !!"
