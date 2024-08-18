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
}


def filenameToTitle(filename: str) -> str:
    title = TITLE_MAPPING.get(filename)
    return title if title is not None else f"!! {filename} !!"
