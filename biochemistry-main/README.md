 # 🧬 Biochemistry Enzyme Database Manager

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![SQL](https://img.shields.io/badge/SQLite-Database-green)
![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-success)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-red)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-purple)

ETL pipeline and query engine for managing biochemical enzyme data using Python and SQL.

---

## 🎯 Problem Statement

Biochemical enzyme datasets are typically provided as raw TSV files containing:

- Multiple substrates and products in a single field  
- Enzyme classification identifiers (EC numbers)  
- Semi-structured biological annotations  

Direct usage of these files makes querying and analysis inefficient.

This project solves that by converting raw biochemical data into a **normalized SQLite database** with a Python-based query interface.

---

## 📖 Project Overview

This system automatically:

- Downloads the latest enzyme dataset
- Cleans and standardizes TSV data
- Converts raw data into structured format
- Stores data in a normalized SQLite database
- Creates separate relational tables for biochemical entities
- Provides a query layer for enzyme retrieval
- Validates outputs using Pydantic models

---

## ✨ Key Features

- Automated dataset download from remote URL  
- SQLite-based relational database design  
- Normalized enzyme, substrate, and product tables  
- Parameterized SQL queries (secure execution)  
- Reverse lookup: product → EC numbers  
- EC number-based enzyme filtering  
- Pydantic-based schema validation  
- Modular ETL pipeline architecture  
- Fully tested with Pytest  

---

## 🛠 Technologies Used

| Category | Technology |
|----------|------------|
| Language | Python |
| Database | SQLite |
| Data Processing | Pandas |
| HTTP Requests | Requests |
| Validation | Pydantic |
| Testing | Pytest |
| File Handling | OS, urllib |

---

## 🧩 Core Components

### 🗄 DatabaseManager

Responsible for ETL operations:

- Downloads enzyme TSV dataset
- Converts TSV → Pandas DataFrame
- Renames and standardizes columns
- Imports data into SQLite
- Extracts structured biological tables

---

### 🔎 QueryManager

Handles all database queries:

- Fetch enzymes by EC number
- Perform product-based reverse lookup
- Maintains SQLite connection and cursor
- Returns validated Python objects

---

### 🧬 EnzymeTableRow (Pydantic Model)

Represents a single enzyme record:

- `id: int`
- `substrates: str`
- `products: str`
- `ec_number: str`
- `enzyme_name: str`

Ensures strict type safety for query results.

---

## 🚀 Example Usage

```python
from biochemistry.manager import DatabaseManager, QueryManager

# Initialize database and import data
db = DatabaseManager(path_to_data_file="data.tsv")
db.download_data()
db.import_data()

# Query enzyme data
query = QueryManager()

results = query.get_enzymes_by_ec_number("1.1.1.1")

for enzyme in results:
    print(enzyme.enzyme_name, enzyme.ec_number)
---
---
## 🧪 Running Tests
pytest
---
## 👨‍💻 Author
Faiza

 
