import sqlite3, pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parents[1]
csv_path = project / "Excel" / "kaggle_income.csv"
df = pd.read_csv(csv_path, encoding="latin1")

with sqlite3.connect(":memory:") as conn:   # use in-memory DB
    df.to_sql("income", conn, if_exists="replace", index=False)

    avg_state = pd.read_sql_query(
        """
        SELECT State_Name, AVG(Median) AS avg_income
        FROM income
        WHERE Median IS NOT NULL
        GROUP BY State_Name
        ORDER BY avg_income DESC;
        """,
        conn
    )
#avg_state.to_csv("resultsState.csv", index=False)

print(avg_state)
