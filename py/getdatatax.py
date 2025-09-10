import pandas as pd

# Construct data for all 50 states + DC with effective property tax rates (approx. 2024/2025 data)
# Sources: Bankrate 2025, WSJ, Business Insider summaries. (Some averages approximated)
data = [
    ("Alabama", 0.41),
    ("Alaska", 0.94),
    ("Arizona", 0.41),
    ("Arkansas", 0.60),
    ("California", 0.69),
    ("Colorado", 0.50),
    ("Connecticut", 1.41),
    ("Delaware", 0.40),
    ("District of Columbia", 0.71),
    ("Florida", 0.79),
    ("Georgia", 0.92),
    ("Hawaii", 0.29),
    ("Idaho", 0.63),
    ("Illinois", 2.29),
    ("Indiana", 0.87),
    ("Iowa", 1.29),
    ("Kansas", 1.33),
    ("Kentucky", 0.83),
    ("Louisiana", 0.55),
    ("Maine", 1.20),
    ("Maryland", 1.09),
    ("Massachusetts", 1.12),
    ("Michigan", 1.54),
    ("Minnesota", 1.00),
    ("Mississippi", 0.65),
    ("Missouri", 0.91),
    ("Montana", 0.83),
    ("Nebraska", 1.54),
    ("Nevada", 0.55),
    ("New Hampshire", 2.09),
    ("New Jersey", 2.46),
    ("New Mexico", 0.80),
    ("New York", 1.64),
    ("North Carolina", 0.77),
    ("North Dakota", 1.01),
    ("Ohio", 1.36),
    ("Oklahoma", 0.90),
    ("Oregon", 0.90),
    ("Pennsylvania", 1.26),
    ("Rhode Island", 1.63),
    ("South Carolina", 0.57),
    ("South Dakota", 1.31),
    ("Tennessee", 0.67),
    ("Texas", 1.90),
    ("Utah", 0.57),
    ("Vermont", 1.78),
    ("Virginia", 0.82),
    ("Washington", 0.93),
    ("West Virginia", 0.59),
    ("Wisconsin", 1.29),
    ("Wyoming", 0.61)
]

# Create DataFrame
df = pd.DataFrame(data, columns=["State", "Effective_Tax_Rate(%)"])


print(f"Property tax rates by state saved to {df.to_csv('Property_Tax_Rates_by_State.csv', index=False)}")