import sqlite3, pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parents[1]
csv_path = project / "Excel" / "poprate.csv"

# 1) Read + clean
df = pd.read_csv(csv_path, encoding="latin1")
df["State"] = df["State"].str.lstrip(".").str.strip()

# 2) Wide → long
df_long = df.melt(
    id_vars=["State"],
    var_name="Year",
    value_name="Population"
)

# 3) Clean numerics
df_long["Population"] = df_long["Population"].str.replace(",", "", regex=False).astype(int)
df_long["Year"] = df_long["Year"].astype(int)

# 4) Pop_Growth (%) year-over-year per state
df_long["Pop_Growth"] = (
    df_long.groupby("State")["Population"].pct_change() * 100
).round(2)

# 5) Save results (optional)
df_long.to_csv(project / "Excel" / "poprate_long.csv", index=False)

avg_growth = (
    df_long.groupby("State", as_index=False)["Pop_Growth"]
           .mean()
           .rename(columns={"Pop_Growth": "Avg_Pop_Growth_%"})
           .sort_values("Avg_Pop_Growth_%", ascending=False)
           .round(2)
)
avg_growth.to_csv(project / "Excel" / "poprate_avg_growth.csv", index=False)

# 6) Print a quick check
#print(df_long.head(12))
print("\nTop states by average yearly population growth (%):")
print(avg_growth)

# make csv file for sql
avg_growth.to_csv("resultsPop.csv", index=False)








