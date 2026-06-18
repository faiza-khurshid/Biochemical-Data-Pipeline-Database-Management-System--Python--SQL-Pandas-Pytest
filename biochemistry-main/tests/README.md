## Practical lab exam

2026-03-19, TSC 1st semester 2nd week

### Allowed Links

1. [os module](https://docs.python.org/3/library/os.html)
2. [requests module](https://docs.python-requests.org/en/latest/)
3. [pandas module](https://pandas.pydata.org/docs/)
4. [sqlite3 module](https://docs.python.org/3/library/sqlite3.html)
5. [pydantic module](https://pydantic-docs.helpmanual.io/)

ALERT: Using any other link is not allowed and will be considered as cheating.

### Instructions

Please read the following instructions carefully before you start working on the tests:

1. Don't change the test functions that are already defined in this file.
2. You can add new test functions if you want to test additional functionality.
   But add this at the end of the file after `# My Tests` comment.

### Tips for implementation

#### Libraries you need
- Use `os` for path handling and directory creation.
- Use `requests` for downloading the data file.
- Use `pandas` for reading the TSV file and handling the DataFrame.
- Use `sqlite3` for database operations.
- Use `pydantic` for defining the `EnzymeTableRow` data model.
- Use `pytest` for running the tests.

#### *constants* module
- Define `HOME`, `DATA_DIR`, `PATH_DOWNLOAD_FILE`, `PATH_DATABASE` using `os.path.expanduser("~")` and `os.path.join`.
- Create `DATA_DIR` with `os.makedirs` if it does not exist.
- Define string constants `TABLE_NAME_ENZYME = "enzyme"`, `TABLE_NAME_SUBSTRATE = "substrate"`, `TABLE_NAME_PRODUCT = "product"`.
- Define a `COLUMNS` dict mapping raw TSV column names (`"ID"`, `"Substrates"`, `"Products"`, `"EC number"`, `"Enzyme name"`) to their snake_case equivalents used in the database.

#### `EnzymeTableRow` in *manager* module
- Subclass `pydantic.BaseModel` with fields: `id: int`, `substrates: str`, `products: str`, `ec_number: str`, `enzyme_name: str`.

#### `DatabaseManager.__init__` in *manager* module
- Accept `path_to_data_file: str` and optional `path_database: str | None = None`.
- If `path_database` is `None`, fall back to `constants.PATH_DATABASE`.
- Open a `sqlite3.connect(self.path_database)` connection and create a cursor.

#### `DatabaseManager.download_data`
- Return `False` (without downloading) if `constants.PATH_DOWNLOAD_FILE` already exists.
- Otherwise use `requests.get(constants.DOWNLOAD_URL, timeout=10)` and write `response.content` to `constants.PATH_DOWNLOAD_FILE` in binary mode; return `True`.

#### `DatabaseManager.get_dataframe_from_data`
- Read the TSV with `pd.read_csv(..., sep="\t", index_col="ID")`.
- Rename columns using `df.rename(columns=constants.COLUMNS, inplace=True)`.
- Rename the index to `"id"` with `df.index.rename("id", inplace=True)`.

#### `DatabaseManager.import_data`
- Call `get_dataframe_from_data()` to obtain the DataFrame.
- Persist it with `df.to_sql(name=constants.TABLE_NAME_ENZYME, con=self.connection, if_exists="replace", index_label="id")`.
- Return the number of rows inserted (query `SELECT COUNT(*) FROM <table>`).

#### `QueryManager.__init__`
- Accept optional `path_database: str | None = None`; fall back to `constants.PATH_DATABASE`.
- Create a `sqlite3.connect` connection, set `connection.row_factory = sqlite3.Row`, and create a cursor.
