import sqlite3, pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parents[1]
csv_path = project / "Excel" / "data.csv"
db_path = project / "py" / "realestate.db"

df = pd.read_csv(csv_path)

with sqlite3.connect(db_path) as conn:
    df.to_sql("houses", conn, if_exists="replace", index=False)

    top10 = pd.read_sql(
        "SELECT price, bed, bath, house_size, city "
        "FROM houses WHERE price IS NOT NULL "
        "ORDER BY price DESC LIMIT 10;", conn)

    avg_state = pd.read_sql(
       "SELECT state, COUNT(*) AS total_houses, AVG(price) AS avg_price "
        "FROM houses WHERE price IS NOT NULL "
        "GROUP BY state ORDER BY avg_price DESC;", conn)
pd.options.display.float_format = '{:,.0f}'.format


#print(top10)
print(avg_state)
avg_state.to_csv("resultsState.csv", index=False)  


