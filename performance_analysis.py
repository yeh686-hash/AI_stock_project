import pandas as pd

# ===== 讀取每日選股 =====

df = pd.read_csv(
    "daily_picks.csv"
)

print("\n===== AI每日選股資料 =====\n")

print(df.head())

print("\n總筆數:", len(df))

# ===== 族群統計 =====

print("\n===== 主流族群統計 =====\n")

sector_count = df["族群"].value_counts()

print(sector_count.head(20))