from biochemistry import constants
import os
import urllib.request
import requests
import pandas as pd
import sqlite3

from pydantic import BaseModel


def get_table_names_from_database(path_database: str) -> set:
    """Get table names from database."""
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()
    return tables


class DatabaseManager:
    def __init__(self, path_to_data_file: str, path_database: str = None):
        self.path_to_data_file = path_to_data_file
        if path_database is None:
            self.path_database = constants.PATH_DATABASE
        else:
            self.path_database = path_database

    def __repr__(self) -> str:
        """Return string representation of DatabaseManager."""

        return f"<DatabaseManager: {self.path_database}>"

    def download_data(self) -> bool:
        """Download data file if it does not exist using requests.

        Returns True if file was downloaded, False if it already existed.
        """
        if os.path.exists(self.path_to_data_file):
            return False

        os.makedirs(os.path.dirname(self.path_to_data_file), exist_ok=True)
        response = requests.get(constants.DOWNLOAD_URL)
        with open(self.path_to_data_file, "wb") as f:
            f.write(response.content)
        return True

    def get_dataframe_from_data(self) -> pd.DataFrame:
        """Read TSV data file and return a formatted DataFrame with renamed columns.

        Returns a DataFrame with columns: substrates, products, ec_number, enzyme_name
        and index named id.
        """
        df = pd.read_csv(self.path_to_data_file, sep="\t", index_col=0)
        df.index.name = "id"
        df.columns = ["substrates", "products", "ec_number", "enzyme_name"]
        return df

    def import_data(self) -> int:
        """Import data from TSV file into the database.

        Returns the number of rows imported.
        """
        df = self.get_dataframe_from_data()
        conn = sqlite3.connect(self.path_database)
        rows = df.to_sql(
            constants.TABLE_NAME_ENZYME, conn, if_exists="replace", index_label="id"
        )
        conn.close()
        return rows


class EnzymeTableRow(BaseModel):
    """Represents a row in the enzyme table."""

    id: int
    substrates: str
    products: str
    ec_number: str
    enzyme_name: str


class QueryManager:
    """Manages database query operations."""

    def __init__(self, path_database: str = None):
        """Initialize QueryManager with optional database path."""
        if path_database is None:
            self.path_database = constants.PATH_DATABASE
        else:
            self.path_database = path_database
        self.connection = sqlite3.connect(self.path_database)
        self.cursor = self.connection.cursor()

    def __repr__(self) -> str:
        """Return string representation of QueryManager."""
        return f"<QueryManager: {self.path_database}>"

    def get_enzymes_by_ec_number(self, ec_number: str) -> list[EnzymeTableRow]:
        """Get all enzymes with the given EC number from the database."""
        self.cursor.execute(
            f"SELECT * FROM {constants.TABLE_NAME_ENZYME} WHERE ec_number = ?",
            (ec_number,),
        )
        rows = self.cursor.fetchall()
        return [
            EnzymeTableRow(
                id=row[0],
                substrates=row[1],
                products=row[2],
                ec_number=row[3],
                enzyme_name=row[4],
            )
            for row in rows
        ]


# from here
