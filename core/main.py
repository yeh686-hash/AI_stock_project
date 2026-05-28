import os
import pandas as pd
from tabulate import tabulate

# ===== 讀取資料夾 =====

data_path = "data/stock_data"

files = os.listdir(data_path)

result_list = []

print("讀取 sector_master.csv")
sector_df = pd.read_csv("sector_master.csv")

print("讀取 industry_master.csv")
industry_df = pd.read_csv("industry_master.csv")

# ===== 股票分析 =====

for file in files:

    try:

        if not file.endswith(".csv"):
            continue

        stock_id = file.replace(".csv", "")

        file_path = os.path.join(
            data_path,
            file
        )

        df = pd.read_csv(file_path)

        # ===== 檢查欄位 =====

        required_columns = [

            "Close",
            "Volume"

        ]

        for col in required_columns:

            if col not in df.columns:

                raise Exception(
                    f"缺少欄位: {col}"
                )

        # ===== 轉數字 =====

        df["Close"] = pd.to_numeric(
            df["Close"],
            errors="coerce"
        )

        df["Volume"] = pd.to_numeric(
            df["Volume"],
            errors="coerce"
        )

        # ===== 去除空值 =====

        df = df.dropna()

        if len(df) < 30:
            continue

        latest = df.iloc[-1]

        close_price = latest["Close"]

        volume = latest["Volume"]

        value = close_price * volume

        ma5 = df["Close"].rolling(5).mean().iloc[-1]

        ma20 = df["Close"].rolling(20).mean().iloc[-1]

        # ===== RSI =====

        delta = df["Close"].diff()

        gain = delta.where(delta > 0, 0)

        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(14).mean()

        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        rsi = round(rsi.iloc[-1], 2)

        # ===== 5日漲幅 =====

        change_5d = round(

            (
                close_price
                / df["Close"].iloc[-6]
                - 1
            ) * 100,

            2

        )

        # ===== AI分數 =====

        score = 0

        if close_price > ma5:
            score += 5

        if close_price > ma20:
            score += 5

        if volume > df["Volume"].rolling(5).mean().iloc[-1]:
            score += 5

        if rsi > 60:
            score += 5

        if change_5d > 3:
            score += 5

        # ===== 股票名稱 =====

        stock_name = ""

        try:

            stock_row = industry_df[
                industry_df["股票代號"].astype(str)
                == stock_id
            ]

            if len(stock_row) > 0:

                stock_name = stock_row.iloc[0]["股票名稱"]

        except:
            pass

        # ===== 產業 =====

        industry = "其他"

        try:

            industry_row = industry_df[
                industry_df["股票代號"].astype(str)
                == stock_id
            ]

            if len(industry_row) > 0:

                industry = industry_row.iloc[0]["產業"]

        except:
            pass

        # ===== 族群 =====

        sector = "其他"

        try:

            sector_row = sector_df[
                sector_df["股票代號"].astype(str)
                == stock_id
            ]

            if len(sector_row) > 0:

                sector = sector_row.iloc[0]["族群"]

        except:
            pass

        # ===== 風險 =====

        risk = "低"

        if rsi > 75:
            risk = "高"

        elif rsi > 65:
            risk = "中"

        result_list.append({

            "代號": stock_id,
            "名稱": stock_name,
            "產業": industry,
            "族群": sector,
            "分數": score,
            "5日漲幅": change_5d,
            "RSI": rsi,
            "成交量": int(volume),
            "成交值": int(value),
            "收盤價": round(close_price, 2),
            "風險": risk

        })

    except Exception as e:

        print("\n===== 錯誤股票 =====")

        print(file)

        print("錯誤原因:")

        print(e)

        continue

# ===== DataFrame =====

result_df = pd.DataFrame(result_list)

# ===== 防止空資料 =====

if len(result_df) == 0:

    print("\n沒有可分析股票")

    exit()

# ===== 排序 =====

result_df = result_df.sort_values(
    by="分數",
    ascending=False
)

# ===== 篩選 =====

pick_df = result_df[
    (result_df["分數"] >= 15)
]

# ===== 顯示 =====

print("\n===== AI選股系統報告 =====\n")

print(f"股票數量: {len(result_df)}")

print(f"符合條件: {len(pick_df)}")

print(

    tabulate(

        pick_df.head(30),

        headers="keys",

        tablefmt="grid",

        showindex=False

    )

)

# ===== 儲存 =====

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

# ===== TXT報告 =====

with open(

    "reports/選股報告.txt",

    "w",

    encoding="utf-8-sig"

) as f:

    f.write("AI選股系統報告\n\n")

    f.write(

        tabulate(

            pick_df.head(30),

            headers="keys",

            tablefmt="grid",

            showindex=False

        )

    )

print("\n每日選股已更新")

print("\n選股結果已輸出")

print("\nTXT報告已輸出")