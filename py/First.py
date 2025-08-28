import sqlite3
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
from pathlib import Path


# Resolve paths relative to this file, not the working directory
current_file_path = Path(__file__).resolve()
project_root_path = current_file_path.parents[1]
excel_directory_path = project_root_path / "Excel"
cvs_input_file_path = excel_directory_path / "csv/data.csv"
output_csv_file_path = excel_directory_path / "top_10_expensive_houses.csv"
database_file_path = current_file_path.parent / "realestate.db"

# Load CSV
df = pd.read_csv(cvs_input_file_path)

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
# Save the results to a new CSV file
#result.to_csv(output_csv_file_path, index=False)

# Close the connection
conn.close()


