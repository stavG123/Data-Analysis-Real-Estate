import sqlite3, pandas as pd
from pathlib import Path

pd.options.display.float_format = '{:,.0f}'.format

# נתיבים
project = Path(__file__).resolve().parents[1]
csv_path = project / "Excel" / "data.csv"
db_path  = project / "py" / "realestate.db"

# קריאה מקורית
df = pd.read_csv(csv_path)

# ניקוי טיפוסים
num_cols = ["price","bed","bath","acre_lot","house_size","zip_code"]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# סינון בסיסי
df = df[(df["price"] > 10000) & (df["house_size"] > 0)]

# חישובים חשובים
df["PricePerSqFt"] = df["price"] / df["house_size"]
df["PricePerBed"]  = df["price"] / df["bed"]
df["PricePerBath"] = df["price"] / df["bath"]

# שמירה ל-SQLite
with sqlite3.connect(db_path) as conn:
    df.to_sql("houses_enriched", conn, if_exists="replace", index=False)

    # ממוצע לפי State
    avg_state = pd.read_sql(
        """
        SELECT state,
               COUNT(*) AS total_houses,
               AVG(price) AS avg_price,
               AVG(PricePerSqFt) AS avg_ppsf
        FROM houses_enriched
        WHERE price IS NOT NULL AND house_size IS NOT NULL AND house_size > 0 and state IS NOT NULL
        GROUP BY state
        ORDER BY avg_ppsf DESC;
        """, conn
    )

    # Top 50 ערים ביוקר אמיתי (PricePerSqFt) עם סף מינימום עסקאות כדי למנוע רעש
    avg_city = pd.read_sql(
        """
        SELECT state, city,
               COUNT(*) AS n_listings,
               AVG(PricePerSqFt) AS avg_ppsf_city
        FROM houses_enriched
        WHERE PricePerSqFt IS NOT NULL
        GROUP BY state, city
        HAVING COUNT(*) >= 20
        ORDER BY avg_ppsf_city DESC
        LIMIT 50;
        """, conn
    )

    # זיפ-קוד יקרים (כשהדאטה איכותי בזיפ)
    avg_zip = pd.read_sql( 
        """
        SELECT state, zip_code,
               COUNT(*) AS n_listings,
               AVG(PricePerSqFt) AS avg_ppsf_zip
        FROM houses_enriched
        WHERE zip_code IS NOT NULL AND PricePerSqFt IS NOT NULL
        GROUP BY state, zip_code
        HAVING COUNT(*) >= 15
        ORDER BY avg_ppsf_zip DESC
        LIMIT 50;
        """, conn
    )

# שמירת קבצים לייצוא (ל-Power BI/Excel)
out_dir = project / "Excel"  # או כל תיקייה שנוחה לך
out_dir.mkdir(parents=True, exist_ok=True)

avg_state.to_csv(out_dir / "results_state_ppsf.csv", index=False)
#avg_city.to_csv(out_dir / "results_city_ppsf_top50.csv", index=False)
#avg_zip.to_csv(out_dir / "results_zip_ppsf_top50.csv", index=False)

print("Saved:",
      out_dir / "results_state_ppsf.csv",
      out_dir / "results_city_ppsf_top50.csv",
      out_dir / "results_zip_ppsf_top50.csv", sep="\n")
