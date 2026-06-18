"""Tests for biochemistry package"""

import os
import sqlite3

import pandas as pd

from biochemistry import constants
from biochemistry.manager import DatabaseManager, QueryManager, EnzymeTableRow

# These are the paths to the test data file and the test database that will
# be used in the tests.
current_folder: str = os.path.dirname(__file__)
test_data_file_path: str = os.path.join(current_folder, "data", "test_data.tsv")
path_test_database: str = os.path.join(constants.DATA_DIR, "test.db")


# Helper function to get the table names from the database
# Don't consider this function for the implementation of the tests, it is only used
# to check if the tables are created correctly in the database.
def get_table_names_from_database(path_database: str) -> set[str]:
    """Get the table names from the database"""
    connection = sqlite3.connect(path_database)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    return {row[0] for row in rows}


def test_constants():
    """Test if all constants exists"""
    assert (
        constants.DOWNLOAD_URL
        == "https://owncloud.scai.fraunhofer.de/s/A5LGNoKeQqMKeYF/download"
    )
    home: str = os.path.expanduser("~")
    assert constants.HOME == home

    # check if the data directory is correct
    data_dir: str = os.path.join(home, ".biochemistry")
    assert constants.DATA_DIR == data_dir

    # check if the path to the download file is correct
    path_download_file: str = os.path.join(data_dir, "data.tsv")
    assert constants.PATH_DOWNLOAD_FILE == path_download_file

    # check if the path to the database is correct
    path_database: str = os.path.join(data_dir, "test.db")
    assert constants.PATH_DATABASE == path_database

    # check if the table names are correct
    assert constants.TABLE_NAME_ENZYME == "enzyme"
    assert constants.TABLE_NAME_SUBSTRATE == "substrate"
    assert constants.TABLE_NAME_PRODUCT == "product"


def test_database_manager_initialization() -> None:
    """Test init of DatabaseManager and QueryManager classes"""
    # intialize the DatabaseManager only with:
    #   1. path_to_data_file: the path to the test data file
    # In this case `dbm.path_to_data_file` should be set to the default value
    # Tip: argument path_database in __init__ function of DatabaseManager class
    # should be optional with a default value None and if it is not provided,
    # it should be set to the default value `constants.PATH_DATABASE`
    dbm2 = DatabaseManager(path_to_data_file=test_data_file_path)
    assert dbm2.path_database == constants.PATH_DATABASE
    assert dbm2.path_to_data_file == test_data_file_path

    # intialize the DatabaseManager with:
    #   1. path_to_data_file: the path to the test data file
    #   2. path_database: the path to the test database
    dbm = DatabaseManager(
        path_to_data_file=test_data_file_path, path_database=path_test_database
    )
    assert dbm.path_database == path_test_database
    assert dbm.path_to_data_file == test_data_file_path


def test_repr_function_of_classes() -> None:
    """Test if __repr__ function of DatabaseManager and QueryManager classes works correctly"""

    # create instances of DatabaseManager and QueryManager classes with the path to the test database
    dbm = DatabaseManager(
        path_to_data_file=path_test_database, path_database=path_test_database
    )
    qm = QueryManager(path_database=path_test_database)

    # The `repr` calls the __repr__ function of the class and
    # returns a string representation of the object

    assert repr(dbm) == f"<DatabaseManager: {path_test_database}>"
    assert repr(qm) == f"<QueryManager: {path_test_database}>"


def test_download_data_if_not_exists() -> None:
    """Test if download_data function of DatabaseManager class downloads file if it does not exist"""
    if os.path.exists(constants.PATH_DOWNLOAD_FILE):
        os.remove(constants.PATH_DOWNLOAD_FILE)
    dbm = DatabaseManager(
        path_to_data_file=constants.PATH_DOWNLOAD_FILE,
        path_database=constants.PATH_DATABASE,
    )
    is_downloaded: bool = dbm.download_data()
    assert is_downloaded
    assert os.path.exists(constants.PATH_DOWNLOAD_FILE)


def test_download_data_if_exists() -> None:
    """Test if download_data function of DatabaseManager class does not download file when it already exists"""
    if os.path.exists(constants.PATH_DOWNLOAD_FILE):
        os.remove(constants.PATH_DOWNLOAD_FILE)
    dbm = DatabaseManager(
        path_to_data_file=constants.PATH_DOWNLOAD_FILE,
        path_database=constants.PATH_DATABASE,
    )
    # download first time
    dbm.download_data()
    # download second time should return False and not download the file again
    is_downloaded: bool = dbm.download_data()
    assert not is_downloaded
    # check if the file exists even it was not downloaded again
    assert os.path.exists(constants.PATH_DOWNLOAD_FILE)


def test_get_dataframe_from_data() -> None:
    """Test if get_dataframe_from_data function of DatabaseManager class works correctly"""
    dbm = DatabaseManager(
        path_to_data_file=test_data_file_path, path_database=path_test_database
    )
    # this needs already renaming of columns
    expected_dataframe = pd.DataFrame(
        data={
            "id": [1, 2, 3],
            "substrates": ["A + B", "C", "D"],
            "products": ["C", "D + E", "F"],
            "ec_number": ["1.1.1.1", "1.1.1.1", "1.1.1.2"],
            "enzyme_name": ["enzyme1", "enzyme2", "enzyme3"],
        }
    ).set_index("id")
    df: pd.DataFrame = dbm.get_dataframe_from_data()
    # checks if get_dataframe_from_data returns a dataframe
    assert isinstance(df, pd.DataFrame)
    # checks if the index name is correct
    assert df.index.name == "id"
    # check for correct column names
    assert set(df.columns) == {"substrates", "products", "ec_number", "enzyme_name"}
    assert df.equals(expected_dataframe)


def test_import_data() -> None:
    """Test if import_data function of DatabaseManager class works correctly"""
    if os.path.exists(path_test_database):
        os.remove(path_test_database)
    dbm = DatabaseManager(
        path_to_data_file=test_data_file_path, path_database=path_test_database
    )
    # inside the function `import_data` make use of `get_dataframe_from_data` function
    # to get the dataframe and then load it in the database.
    # in function `pd.to_sql` argument `index_label` should be set to "id" and
    # `if_exists` should be set to "replace"
    assert dbm.import_data() == 3
    assert get_table_names_from_database(path_test_database) == {
        constants.TABLE_NAME_ENZYME
    }


def test_enzyme_table_row() -> None:
    """Test if EnzymeTableRow class works correctly

    Tip: EnzymeTableRow class should be a subclass of `pydantic.BaseModel` and should have the following attributes:
        - id: int
        - substrates: str
        - products: str
        - ec_number: str
        - enzyme_name: str

    """
    enzyme_row = EnzymeTableRow(
        id=1,
        substrates="A + B",
        products="C",
        ec_number="1.1.1.1",
        enzyme_name="enzyme1",
    )
    assert enzyme_row.id == 1
    assert enzyme_row.substrates == "A + B"
    assert enzyme_row.products == "C"
    assert enzyme_row.ec_number == "1.1.1.1"
    assert enzyme_row.enzyme_name == "enzyme1"


def test_query_manager_init() -> None:
    """Test if all QueryManager attributes are initialized correctly"""
    query = QueryManager(path_database=path_test_database)
    assert query.path_database == path_test_database
    assert isinstance(query.connection, sqlite3.Connection)
    assert isinstance(query.cursor, sqlite3.Cursor)


def test_get_enzymes_by_ec_number() -> None:
    """Test if get_enzymes_by_ec_number function of QueryManager class works correctly"""
    DatabaseManager(
        path_to_data_file=test_data_file_path, path_database=path_test_database
    ).import_data()
    query = QueryManager(path_database=path_test_database)
    enzyme_rows: list[EnzymeTableRow] = query.get_enzymes_by_ec_number("1.1.1.1")
    assert len(enzyme_rows) == 2
    assert {enzyme_row.enzyme_name for enzyme_row in enzyme_rows} == {
        "enzyme1",
        "enzyme2",
    }


#################################################################################################
# Extra points for testing the extract_substrates and extract_products functions of DatabaseManager class
#################################################################################################


def test_extract_substrates_and_products() -> None:
    """Test if extract_substrates and extract_products functions of DatabaseManager class work correctly

    Tip: in the functions `extract_substrates` and `extract_products` make use of
    `get_dataframe_from_data` function to get the dataframe and then extract the
    substrates and products from the dataframe. The substrates and products are
    separated by " + " in the dataframe and should be split and exploded to create
    a new table for substrates and products. In function `pd.to_sql` argument
    `index_label` should be set to "id" and `if_exists` should be set to "replace".

    """
    if os.path.exists(path_test_database):
        os.remove(path_test_database)
    dbm = DatabaseManager(
        path_to_data_file=test_data_file_path, path_database=path_test_database
    )
    dbm.import_data()
    assert dbm.extract_substrates() == 4
    assert dbm.extract_products() == 4
    assert get_table_names_from_database(path_test_database) == {
        constants.TABLE_NAME_ENZYME,
        constants.TABLE_NAME_SUBSTRATE,
        constants.TABLE_NAME_PRODUCT,
    }


def test_get_ec_numbers_by_product() -> None:
    """Test if the extracted substrates and products can be queried correctly"""
    query = QueryManager(path_database=path_test_database)
    assert query.get_ec_numbers_by_product("C") == {"1.1.1.1"}
    # check if the products are extracted correctly
    assert query.get_ec_numbers_by_product("F") == {"1.1.1.2"}


# My Tests (Optional)
# ===================
# Here is space to implement your own tests. You can test any function or class that you think is important to test,
# but you don't have to.
# You can also test edge cases and error handling (if you want).
# The more tests you implement, the better the coverage of the code will be.
