import pandas as pd
import os
from tabulate import tabulate

print("讀取 sector_master.csv")
print("讀取 industry_master.csv")

sector_map = {}
industry_map = {}

# ===== 讀取乾淨版族群資料庫 =====

if os.path.exists("sector_master.csv"):

    sector_df = pd.read_csv(
        "sector_master.csv"
    )

    for _, row in sector_df.iterrows():

        try:

            stock_id = str(
                int(row["股票代號"])
            )

            sector_map[stock_id] = row["族群"]

        except:
            continue


# ===== 讀取乾淨版產業資料庫 =====

if os.path.exists("industry_master.csv"):

    industry_df = pd.read_csv(
        "industry_master.csv"
    )

    for _, row in industry_df.iterrows():

        try:

            stock_id = str(
                int(row["股票代號"])
            )

            industry_map[stock_id] = row["產業"]

        except:
            continue


# ===== 讀取技術資料 =====

df = pd.read_csv(
    "all_stocks.csv"
)

results = []

# ===== 選股 =====

for _, row in df.iterrows():

    try:

        stock_id = str(
            int(row["股票代號"])
        )

        close = float(row["收盤價"])
        ma5 = float(row["MA5"])
        ma20 = float(row["MA20"])
        ma60 = float(row["MA60"])

        volume = float(row["成交量"])
        amount = float(row["成交值"])
        volume_ma5 = float(row["量MA5"])

        rsi = float(row["RSI"])
        change = float(row["5日漲幅"])

        # ===== 排除權證 =====

        if stock_id.startswith("7"):
            continue

        if stock_id.startswith("9"):
            continue

        score = 0

        # ===== 均線 =====

        if close > ma5:
            score += 3

        if close > ma20:
            score += 5

        if close > ma60:
            score += 5

        if ma5 > ma20:
            score += 3

        # ===== 量能 =====

        if volume > volume_ma5 * 1.5:
            score += 3

        # ===== RSI =====

        if rsi > 55:
            score += 3

        if rsi > 65:
            score += 3

        # ===== 漲幅 =====

        if change > 10:
            score += 2

        if change > 20:
            score += 2

        # ===== 成交值 =====

        if amount > 300000000:
            score += 3

        elif amount > 100000000:
            score += 2

        # ===== 過熱排除 =====

        if rsi > 85:
            continue

        if change > 35:
            continue

        # ===== 族群 =====

        sector = sector_map.get(
            stock_id,
            "其他"
        )

        # ===== AI主流加分 =====

        strong_sectors = [

            "AI伺服器",
            "工業電腦",
            "CPO",
            "CoWoS",
            "BBU",
            "散熱",
            "高速傳輸",
            "矽光子",
            "AI電源",
            "機器人",
            "網通",
            "封測",
            "DRAM",
            "矽智財",
            "ASIC"

        ]

        if sector in strong_sectors:
            score += 3

        # ===== 產業 =====

        industry = industry_map.get(
            stock_id,
            "其他"
        )

        # ===== 風險 =====

        risk = "低"

        if rsi > 75:
            risk = "高"

        elif rsi > 65:
            risk = "中"

        # ===== 篩選 =====

        if score >= 9:

            results.append([

                stock_id,
                industry,
                sector,
                score,
                round(change, 2),
                round(rsi, 2),
                int(volume),
                int(amount),
                risk

            ])

    except:
        continue


# ===== DataFrame =====

result_df = pd.DataFrame(

    results,

    columns=[

        "代號",
        "產業",
        "族群",
        "分數",
        "5日漲幅",
        "RSI",
        "成交量",
        "成交值",
        "風險"

    ]

)

# ===== 排序 =====

result_df = result_df.sort_values(

    by=[
        "分數",
        "成交值"
    ],

    ascending=False

)

# ===== 主流族群熱度 =====

print("\n===== 主流族群熱度 =====\n")

sector_rows = []

for sector in result_df["族群"].value_counts().index:

    temp = result_df[
        result_df["族群"] == sector
    ]

    avg_score = round(
        temp["分數"].mean(),
        2
    )

    avg_change = round(
        temp["5日漲幅"].mean(),
        2
    )

    avg_amount = int(
        temp["成交值"].mean()
    )

    count = len(temp)

    strong_ratio = round(

        len(
            temp[temp["分數"] >= 25]
        ) / count * 100,

        1

    )

    # ===== 星數 =====

    if avg_score >= 25 and avg_amount > 300000000:
        stars = "5星"

    elif avg_score >= 22:
        stars = "4星"

    elif avg_score >= 18:
        stars = "3星"

    elif avg_score >= 14:
        stars = "2星"

    else:
        stars = "1星"

    sector_rows.append([

        sector,
        stars,
        count,
        avg_score,
        f"{avg_change}%",
        f"{avg_amount:,}",
        f"{strong_ratio}%"

    ])

sector_df = pd.DataFrame(

    sector_rows,

    columns=[

        "族群",
        "熱度",
        "檔數",
        "平均分數",
        "平均漲幅",
        "平均成交值",
        "強勢比"

    ]

)

# ===== 星數排序 =====

star_order = {

    "5星": 5,
    "4星": 4,
    "3星": 3,
    "2星": 2,
    "1星": 1

}

sector_df["排序"] = sector_df["熱度"].map(
    star_order
)

sector_df = sector_df.sort_values(

    by=[
        "排序",
        "平均分數"
    ],

    ascending=False

)

sector_df = sector_df.drop(
    columns=["排序"]
)

# ===== 主流表格 =====

sector_table = tabulate(

    sector_df,

    headers="keys",

    tablefmt="grid",

    showindex=False,

    stralign="center",

    numalign="center"

)

print(sector_table)

# ===== TOP30 =====

print("\n===== TOP30主流集中度 =====\n")

top30 = result_df.head(30)

sector_top30 = top30["族群"].value_counts()

top30_rows = []

for sector, count in sector_top30.items():

    top30_rows.append([
        sector,
        count
    ])

top30_df = pd.DataFrame(

    top30_rows,

    columns=[
        "族群",
        "TOP30檔數"
    ]

)

top30_table = tabulate(

    top30_df,

    headers="keys",

    tablefmt="grid",

    showindex=False,

    stralign="center",

    numalign="center"

)

print(top30_table)

# ===== AI選股報告 =====

print("\n===== AI選股系統報告 =====\n")

print(f"股票數量: {len(df)}")
print(f"符合條件: {len(result_df)}")

show_df = result_df.head(30).copy()

show_df.insert(
    0,
    "排名",
    range(1, len(show_df) + 1)
)

table_text = tabulate(

    show_df,

    headers="keys",

    tablefmt="grid",

    showindex=False,

    stralign="center",

    numalign="center"

)

print(table_text)

# ===== 輸出CSV =====

result_df.to_csv(

    "選股結果.csv",

    index=False,

    encoding="utf-8-sig"

)

# ===== 輸出TXT =====

with open(

    "選股報告.txt",

    "w",

    encoding="utf-8-sig"

) as f:

    f.write("===== AI選股完整報告 =====\n\n")

    f.write(f"股票總數: {len(df)}\n")

    f.write(f"符合條件: {len(result_df)}\n\n")

    f.write("===== 主流族群熱度 =====\n\n")

    f.write(sector_table)

    f.write("\n\n===== TOP30主流集中度 =====\n\n")

    f.write(top30_table)

    f.write("\n\n===== AI選股系統報告 =====\n\n")

    f.write(table_text)

print("\n選股結果已輸出")
print("TXT報告已輸出")