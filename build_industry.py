import os
import pandas as pd

print("建立 industry_master.csv ...")

# ===== 讀取股票主檔 =====

stock_df = pd.read_csv(
    "stock_list.csv",
    encoding="utf-8-sig"
)

stock_df["股票代號"] = (
    stock_df["股票代號"]
    .astype(str)
    .str.zfill(4)
)

# ===== 產業資料夾 =====

industry_path = "config/industry"

all_data = []

# ===== 掃描所有產業CSV =====

for file in os.listdir(industry_path):

    if not file.endswith(".csv"):
        continue

    industry_name = file.replace(".csv", "")

    file_path = os.path.join(
        industry_path,
        file
    )

    try:

        df = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )

        if "股票代號" not in df.columns:
            continue

        df["股票代號"] = (
            df["股票代號"]
            .astype(str)
            .str.zfill(4)
        )

        for stock_id in df["股票代號"]:

            stock_row = stock_df[
                stock_df["股票代號"] == stock_id
            ]

            if len(stock_row) == 0:
                continue

            stock_name = stock_row.iloc[0]["股票名稱"]

            all_data.append([
                stock_id,
                stock_name,
                industry_name
            ])

    except Exception as e:

        print(f"{file} 錯誤: {e}")

# ===== 建立 DataFrame =====

industry_df = pd.DataFrame(

    all_data,

    columns=[
        "股票代號",
        "股票名稱",
        "產業"
    ]

)

industry_df = industry_df.sort_values(
    by=["產業", "股票代號"]
)

# ===== 輸出 =====

industry_df.to_csv(

    "industry_master.csv",

    index=False,

    encoding="utf-8-sig"

)

print()

print(
    f"產業數量: {industry_df['產業'].nunique()}"
)

print(
    f"股票筆數: {len(industry_df)}"
)

print()

print(
    "industry_master.csv 已更新"
)