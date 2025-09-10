import sqlite3, pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parents[1]
csv_path = project / "Excel" / "Unemploy.csv"
df = pd.read_csv(csv_path, encoding="latin1")

with sqlite3.connect(":memory:") as conn:
    df.to_sql("Unemploy", conn, if_exists="replace", index=False)

    # Average unemployment rate per state in 2022
    sql = """
    SELECT
    "State/Area"  AS state,
    AVG("Percent(%)ofLaborForceUnemployedinState/Area") AS avg_unemp_2022
    FROM Unemploy
    WHERE Year = 2022
    GROUP BY "State/Area"
    ORDER BY avg_unemp_2022 DESC;
    """
    Unemploy = pd.read_sql_query(sql, conn)

print(Unemploy)

# make csv file for sql
Unemploy.to_csv("resultsUnem.csv", index=False)
