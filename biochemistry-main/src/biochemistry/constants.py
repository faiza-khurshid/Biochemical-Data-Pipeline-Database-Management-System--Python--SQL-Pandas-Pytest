import os

"""Module containing constants for the biochemistry project."""

HOME = os.path.expanduser("~")
DATA_DIR = os.path.join(HOME, ".biochemistry")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


DOWNLOAD_URL = "https://owncloud.scai.fraunhofer.de/s/A5LGNoKeQqMKeYF/download"
PATH_DOWNLOAD_FILE = os.path.join(DATA_DIR, "data.tsv")
PATH_DATABASE: str = os.path.join(DATA_DIR, "test.db")
TABLE_NAME_ENZYME = "enzyme"
TABLE_NAME_SUBSTRATE = "substrate"
TABLE_NAME_PRODUCT = "product"
