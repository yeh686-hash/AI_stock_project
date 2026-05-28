import pandas as pd
import os
import glob
import ta

# ===== 股票名稱對照 =====

stock_info = pd.read_csv(
    "stock_list.csv"
)

name_map = {}

for _, row in stock_info.iterrows():

    try:

        stock_id = str(
            int(row["股票代號"])
        )

        stock_name = str(
            row["股票名稱"]
        )

        name_map[stock_id] = stock_name

    except:
        continue


all_data = []

# ===== 讀取所有股票資料 =====

files = glob.glob("stock_data/*.csv")

for file in files:

    try:

        df = pd.read_csv(file)

        if len(df) < 60:
            continue

        stock_id = os.path.basename(file).replace(".csv", "")

        stock_id = stock_id.split(".")[0]

        stock_name = name_map.get(
            stock_id,
            ""
        )

        print(f"處理中: {stock_id}")

        # ===== Yahoo欄位 =====

        close = df["Close"]

        volume = df["Volume"]

        # ===== 成交值估算 =====

        amount = close * volume

        # ===== 技術指標 =====

        ma5 = close.rolling(5).mean().iloc[-1]

        ma20 = close.rolling(20).mean().iloc[-1]

        ma60 = close.rolling(60).mean().iloc[-1]

        volume_ma5 = volume.rolling(5).mean().iloc[-1]

        rsi = ta.momentum.RSIIndicator(
            close,
            window=14
        ).rsi().iloc[-1]

        change = (
            (
                close.iloc[-1]
                -
                close.iloc[-6]
            )
            /
            close.iloc[-6]
        ) * 100

        all_data.append({

            "股票代號": stock_id,
            "股票名稱": stock_name,
            "收盤價": round(close.iloc[-1], 2),
            "MA5": round(ma5, 2),
            "MA20": round(ma20, 2),
            "MA60": round(ma60, 2),
            "成交量": int(volume.iloc[-1]),
            "成交值": int(amount.iloc[-1]),
            "量MA5": int(volume_ma5),
            "RSI": round(rsi, 2),
            "5日漲幅": round(change, 2)

        })

    except Exception as e:

        print(f"\n錯誤檔案: {file}")

        print(e)

        continue


# ===== DataFrame =====

result_df = pd.DataFrame(all_data)

print(f"\n成功股票數量: {len(result_df)}")

# ===== 儲存 =====

result_df.to_csv(

    "all_stocks.csv",

    index=False,

    encoding="utf-8-sig"

)

print("\nall_stocks.csv 已更新")