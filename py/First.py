import sqlite3
import pandas as pd
from pathlib import Path
# import matplotlib.pyplot as plt  # optional; not used

# Resolve paths based on this file location (works from any CWD)
current_file_path = Path(__file__).resolve()
project_root_path = current_file_path.parents[1]

excel_directory_path = project_root_path / "Excel"
csv_input_file_path = excel_directory_path / "data.csv"
output_csv_file_path = excel_directory_path / "top_10_expensive_houses.csv"

# Put the DB in the project (not inside Excel)
database_file_path = project_root_path / "py" / "realestate.db"

# Safety check so path issues are obvious
print("Looking for CSV at:", csv_input_file_path)
if not csv_input_file_path.exists():
    raise FileNotFoundError(f"Missing file: {csv_input_file_path}")

# Load CSV
df = pd.read_csv(csv_input_file_path)

# Connect to SQLite (creates file if not exists)
conn = sqlite3.connect(str(database_file_path))

# Write DataFrame into SQL table
df.to_sql("houses", conn, if_exists="replace", index=False)

# Set float format for better readability
pd.set_option("display.float_format", lambda x: f"{x:,.0f}")

# Query top 10 most expensive houses
query = """
SELECT price, bed, bath, house_size, city, state, zip_code, status, brokered_by
FROM houses
WHERE price IS NOT NULL
ORDER BY price DESC
LIMIT 10;
"""
result = pd.read_sql(query, conn)
print(result)

# Optionally save results:
# result.to_csv(output_csv_file_path, index=False)

conn.close()
