import os
import time
import pandas as pd
import yfinance as yf

# ===== 讀取股票清單 =====

stock_df = pd.read_csv(

    "stock_list.csv"

)

# ===== 建立資料夾 =====

os.makedirs(

    "data/stock_data",

    exist_ok=True

)

# ===== 更新資料 =====

for _, row in stock_df.iterrows():

    try:

        stock_id = str(

            row["股票代號"]

        )

        stock_name = str(

            row["股票名稱"]

        )

        # ===== 排除權證與特殊商品 =====

        if stock_id.startswith("7"):
            continue

        if len(stock_id) != 4:
            continue

        # ===== 股票代號 =====

        symbol = stock_id + ".TW"

        print(f"更新中: {symbol}")

        # ===== 抓資料 =====

        df = yf.download(

            symbol,

            period="2y",

            progress=False

        )

        # ===== 無資料 =====

        if df.empty:

            symbol = stock_id + ".TWO"

            print(f"改抓上櫃: {symbol}")

            df = yf.download(

                symbol,

                period="2y",

                progress=False

            )

        # ===== 還是無資料 =====

        if df.empty:

            print(f"{stock_id}.csv 無資料")

            continue

        # ===== 儲存 =====

        file_path = os.path.join(

            "data/stock_data",

            f"{stock_id}.csv"

        )

        df.to_csv(

            file_path,

            encoding="utf-8-sig"

        )

        print(f"{stock_id}.csv 完成")

        # ===== 避免過快 =====

        time.sleep(0.5)

    except Exception as e:

        print(f"{stock_id} 錯誤: {e}")

        continue

print("\n全部股票更新完成")