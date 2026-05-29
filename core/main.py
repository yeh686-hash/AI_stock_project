import os
import pandas as pd
from tabulate import tabulate

# =====================
# 讀取主檔
# =====================

DATA_PATH = "stock_data"
print("讀取 stock_list.csv")
stock_df = pd.read_csv(
    "stock_list.csv",
    encoding="utf-8-sig"
)

print("讀取 industry_master.csv")
industry_df = pd.read_csv(
    "industry_master.csv",
    encoding="utf-8-sig"
)

print("讀取 sector_master.csv")
sector_df = pd.read_csv(
    "sector_master.csv",
    encoding="utf-8-sig"
)

# 股票名稱

stock_df["股票代號"] = (
    stock_df["股票代號"]
    .astype(str)
    .str.zfill(4)
)

industry_df["股票代號"] = (
    industry_df["股票代號"]
    .astype(str)
    .str.zfill(4)
)
name_map = dict(
    zip(
        stock_df["股票代號"].astype(str).str.zfill(4),
        stock_df["股票名稱"]
    )
)

# 產業

industry_map = dict(
    zip(
        industry_df["股票代號"].astype(str).str.zfill(4),
        industry_df["產業"]
    )
)

# 族群

sector_df["股票代號"] = (
    sector_df["股票代號"]
    .astype(str)
    .str.zfill(4)
)

sector_map = (
    sector_df
    .groupby("股票代號")["族群"]
    .apply(lambda x: "|".join(sorted(set(x))))
    .to_dict()
)
result_list = []

# =====================
# 開始分析
# =====================

files = [
    f for f in os.listdir(DATA_PATH)
    if f.endswith(".csv")
]

for file in files:

    try:

        stock_id = file.replace(".csv", "")

        file_path = os.path.join(
            DATA_PATH,
            file
        )

        # Yahoo 新格式

        df = pd.read_csv(
            file_path,
            skiprows=[1]
        )

        required_cols = [
            "Close",
            "Volume"
        ]

        if not all(
            col in df.columns
            for col in required_cols
        ):
            continue

        df["Close"] = pd.to_numeric(
            df["Close"],
            errors="coerce"
        )

        df["Volume"] = pd.to_numeric(
            df["Volume"],
            errors="coerce"
        )

        df = df.dropna()

        if len(df) < 60:
            continue

        close = df["Close"]

        volume = df["Volume"]

        latest_close = close.iloc[-1]
        latest_volume = volume.iloc[-1]

        amount = latest_close * latest_volume

        ma5 = close.rolling(5).mean().iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]

        # RSI

        delta = close.diff()

        gain = delta.where(
            delta > 0,
            0
        )

        loss = -delta.where(
            delta < 0,
            0
        )

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (
            100 / (1 + rs)
        )

        rsi = round(
            rsi.iloc[-1],
            2
        )

        # 五日漲幅

        change_5d = round(

            (
                latest_close
                /
                close.iloc[-6]
                - 1
            ) * 100,

            2

        )

        # =====================
        # AI評分
        # =====================

        score = 0

        if latest_close > ma5:
            score += 5

        if latest_close > ma20:
            score += 5

        if latest_volume > volume.rolling(5).mean().iloc[-1]:
            score += 5

        if rsi > 60:
            score += 5

        if change_5d > 3:
            score += 5

        # =====================
        # 風險
        # =====================

        risk = "低"

        if rsi > 75:
            risk = "高"

        elif rsi > 65:
            risk = "中"

        # =====================
        # 主檔資料
        # =====================

        stock_name = name_map.get(
            stock_id,
            ""
        )

        industry = industry_map.get(
            stock_id,
            "其他"
        )

        sector = sector_map.get(
            stock_id,
            "其他"
        )

        result_list.append({

            "代號": stock_id,
            "名稱": stock_name,
            "產業": industry,
            "族群": sector,
            "分數": score,
            "5日漲幅": change_5d,
            "RSI": rsi,
            "成交量": int(latest_volume),
            "成交值": int(amount),
            "收盤價": round(
                latest_close,
                2
            ),
            "風險": risk

        })

    except Exception as e:

        print(
            f"{file} 錯誤: {e}"
        )

# =====================
# DataFrame
# =====================

result_df = pd.DataFrame(
    result_list
)

if len(result_df) == 0:

    print("\n沒有可分析股票")
    exit()

# =====================
# 排序
# =====================

result_df = result_df.sort_values(
    by="分數",
    ascending=False
)

pick_df = result_df[
    result_df["分數"] >= 15
]

# =====================
# 顯示結果
# =====================

print("\n===== AI選股系統報告 =====\n")

print(
    f"股票數量: {len(result_df)}"
)

print(
    f"符合條件: {len(pick_df)}"
)

print(

    tabulate(

        pick_df.head(30),

        headers="keys",

        tablefmt="grid",

        showindex=False

    )

)

# =====================
# 建立 reports
# =====================

os.makedirs(
    "reports",
    exist_ok=True
)

pick_df.to_csv(

    "reports/daily_picks.csv",

    index=False,

    encoding="utf-8-sig"

)

pick_df.to_csv(

    "reports/選股結果.csv",

    index=False,

    encoding="utf-8-sig"

)

with open(

    "reports/選股報告.txt",

    "w",

    encoding="utf-8-sig"

) as f:

    f.write(
        tabulate(
            pick_df.head(30),
            headers="keys",
            tablefmt="grid",
            showindex=False
        )
    )

print("\n每日選股已更新")
print("選股結果已輸出")
print("TXT報告已輸出")