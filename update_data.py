import os
import pandas as pd
import yfinance as yf

# ===== 讀股票清單 =====

stock_df = pd.read_csv(
    "stock_list.csv",
    header=None
)

# ===== 清理股票代號 =====

stocks = stock_df[
    0
].astype(str).str.strip().str.replace(
    ".0",
    "",
    regex=False
).tolist()

# ===== 建立資料夾 =====

os.makedirs(
    "stock_data",
    exist_ok=True
)

print("\n開始更新股票資料...\n")

# ===== 更新資料 =====

for stock_id in stocks:

    try:

        # ===== 判斷上市 / 上櫃 =====

        ticker = stock_id + ".TW"

        if stock_id.startswith(
            (
                "3",
                "4",
                "5",
                "6",
                "7",
                "8"
            )
        ):

            ticker = stock_id + ".TWO"

        print(
            f"更新中: {ticker}"
        )

        # ===== 下載資料 =====

        df = yf.download(

            ticker,

            period="2y",

            auto_adjust=False,

            progress=False

        )

        # ===== 無資料 =====

        if df.empty:

            print(
                f"{stock_id}.csv 無資料"
            )

            continue

        # ===== 修正 MultiIndex =====

        if isinstance(
            df.columns,
            pd.MultiIndex
        ):

            df.columns = df.columns.get_level_values(0)

        # ===== 重設索引 =====

        df.reset_index(
            inplace=True
        )

        # ===== 修正 Date 欄位 =====

        if "index" in df.columns:

            df.rename(

                columns={
                    "index": "Date"
                },

                inplace=True

            )

        # ===== 檢查必要欄位 =====

        required_columns = [

            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"

        ]

        missing = [

            col for col in required_columns
            if col not in df.columns

        ]

        if missing:

            print(
                f"{stock_id}.csv 缺少欄位: {missing}"
            )

            continue

        # ===== 存檔 =====

        df.to_csv(

            f"stock_data/{stock_id}.csv",

            index=False,

            encoding="utf-8-sig"

        )

        print(
            f"{stock_id}.csv 完成"
        )

    except Exception as e:

        print(
            f"{stock_id}.csv 失敗"
        )

        print(e)

print(
    "\n全部更新完成"
)