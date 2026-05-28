import os
import pandas as pd

results = []

folder = "stock_data"

for file in os.listdir(folder):

    if not file.endswith(".csv"):

        continue

    try:

        stock_id = file.replace(".csv", "")

        df = pd.read_csv(

            f"{folder}/{file}"

        )

        if len(df) < 60:

            continue


        # ===== 數值 =====

        close = pd.to_numeric(

            df["Close"],

            errors="coerce"

        )

        volume = pd.to_numeric(

            df["Volume"],

            errors="coerce"

        )


        # ===== 最新資料 =====

        latest_close = close.iloc[-1]

        latest_volume = volume.iloc[-1]


        # ===== 成交值 =====

        latest_amount = (

            latest_close *

            latest_volume

        )


        # ===== 均線 =====

        ma5 = close.rolling(5).mean()

        ma20 = close.rolling(20).mean()

        ma60 = close.rolling(60).mean()

        volume_ma5 = volume.rolling(5).mean()


        # ===== RSI =====

        delta = close.diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()

        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (

            100 / (1 + rs)

        )

        latest_rsi = rsi.iloc[-1]


        # ===== 5日漲幅 =====

        change_percent = (

            (latest_close - close.iloc[-6])

            / close.iloc[-6]

        ) * 100


        # ===== 加入結果 =====

        results.append([

            stock_id,

            latest_close,

            ma5.iloc[-1],

            ma20.iloc[-1],

            ma60.iloc[-1],

            latest_volume,

            latest_amount,

            volume_ma5.iloc[-1],

            latest_rsi,

            change_percent

        ])

    except:

        continue


# ===== DataFrame =====

result_df = pd.DataFrame(

    results,

    columns=[

        "股票代號",

        "收盤價",

        "MA5",

        "MA20",

        "MA60",

        "成交量",

        "成交值",

        "量MA5",

        "RSI",

        "5日漲幅"

    ]

)


# ===== 輸出 =====

result_df.to_csv(

    "all_stocks.csv",

    index=False,

    encoding="utf-8-sig"

)

print("\nall_stocks.csv 建立完成")