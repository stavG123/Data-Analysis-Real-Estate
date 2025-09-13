import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

project = Path(__file__).resolve().parents[1]
csv_path = project / "Excel" / "Analysis.csv"
# נטען את הקובץ שלך (נניח שזה CSV עם הטבלה שלך)
df = pd.read_csv(csv_path)

# נוריד עמודות לא מספריות (אם יש למשל State_Name)
numeric_df = df.select_dtypes(include=['number'])

# נחשב את מטריצת המתאמים
corr = numeric_df.corr()

# נציג כטבלה
#print(corr)

# נצייר Heatmap
#plt.figure(figsize=(12,8))
#sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
#plt.title("Correlation Matrix of State Housing Data", fontsize=16)
#plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === 1) Load & sanitize ===
df = pd.read_csv(csv_path)

# make sure column names exist (adjust here if needed)
needed = ["State_Name","avg_income","avg_ppsf",
          "Price_to_Income(how many yearly incomes for an average house.)",
          "Effective_Tax_Rate(%)"]
missing = [c for c in needed if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

df = df.dropna(subset=["avg_income","avg_ppsf",
                       "Price_to_Income(how many yearly incomes for an average house.)"])

# keep only plausible ranges
df = df[(df["avg_income"]>0) & (df["avg_ppsf"]>0)]

# === 2) Bubble size: scale Price_to_Income to pixels ===
pti = df["Price_to_Income(how many yearly incomes for an average house.)"].clip(upper=df["Price_to_Income(how many yearly incomes for an average house.)"].quantile(0.98))
pti_norm = (pti - pti.min()) / (pti.max() - pti.min() + 1e-9)
sizes = 200 + 2200 * pti_norm  # 200–2400 pts^2

# optional: annotate a few extremes (top by Y and by PTI)
top_price = df.nlargest(5, "avg_ppsf")
top_pti   = df.nlargest(5, "Price_to_Income(how many yearly incomes for an average house.)")
to_annotate = pd.concat([top_price, top_pti]).drop_duplicates(subset=["State_Name"])

# === 3) Plot ===
plt.figure(figsize=(11,8))
plt.scatter(df["avg_income"], df["avg_ppsf"], s=sizes, alpha=0.7)

plt.xlabel("Median / Avg Income (USD)")
plt.ylabel("Average $ per SqFt")
plt.title("Housing Affordability Bubble Chart by State\n(X=Income, Y=$/SqFt, Bubble Size=Price-to-Income)")

# annotate selected states
for _, r in to_annotate.iterrows():
    plt.annotate(r["State_Name"],
                 (r["avg_income"], r["avg_ppsf"]),
                 xytext=(6,6), textcoords="offset points", fontsize=9)

# helper lines: medians
plt.axvline(df["avg_income"].median(), linestyle="--", linewidth=1)
plt.axhline(df["avg_ppsf"].median(), linestyle="--", linewidth=1)

plt.tight_layout()
plt.show()

# === 4) Quick correlations to guide the eye ===
print("corr(avg_income, avg_ppsf) =",
      df["avg_income"].corr(df["avg_ppsf"]).round(3))
print("corr(Price_to_Income, avg_ppsf) =",
      df["Price_to_Income(how many yearly incomes for an average house.)"].corr(df["avg_ppsf"]).round(3))

