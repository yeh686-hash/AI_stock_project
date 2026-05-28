import pandas as pd

# ===== 讀取觀察名單 =====

df = pd.read_csv(
    "watchlist.csv"
)

print("\n===== AI市場情緒分析 =====\n")

# ===== S級數量 =====

s_count = len(

    df[
        df["AI等級"] == "S"
    ]

)

# ===== 平均分數 =====

avg_score = round(

    df["分數"].mean(),

    2

)

# ===== 主流數量 =====

sector_count = len(

    df["族群"].unique()

)

# ===== 市場情緒 =====

sentiment = "普通"

if s_count >= 5 and avg_score >= 28:

    sentiment = "市場極強"

elif s_count >= 3:

    sentiment = "市場偏強"

elif avg_score < 22:

    sentiment = "市場疲弱"

# ===== 顯示 =====

print(f"S級股票數量: {s_count}")

print(f"平均分數: {avg_score}")

print(f"主流族群數量: {sector_count}")

print(f"\n市場情緒: {sentiment}")

# ===== 建議 =====

print("\n===== AI操作建議 =====\n")

if sentiment == "市場極強":

    print("可積極操作主流股")

elif sentiment == "市場偏強":

    print("可偏多操作")

elif sentiment == "市場疲弱":

    print("降低持股水位")

else:

    print("中性操作")