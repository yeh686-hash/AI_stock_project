import os
import pandas as pd

print("建立 sector_master.csv ...")

# ===== 讀取股票主檔 =====

industry_df = pd.read_csv(
    "industry_master.csv",
    encoding="utf-8-sig"
)

industry_df["股票代號"] = (
    industry_df["股票代號"]
    .astype(str)
    .str.zfill(4)
)

# ===== 族群資料夾 =====

sector_path = "config/sector"

all_data = []

# ===== 掃描所有族群CSV =====

for file in os.listdir(sector_path):

    if not file.endswith(".csv"):
        continue

    sector_name = (
        file
        .replace(".csv", "")
    )

    file_path = os.path.join(
        sector_path,
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

            all_data.append([
                stock_id,
                sector_name
            ])

    except Exception as e:

        print(
            f"{file} 錯誤: {e}"
        )

# ===== 合併 =====

sector_df = pd.DataFrame(

    all_data,

    columns=[
        "股票代號",
        "族群"
    ]

)

result_df = sector_df.merge(

    industry_df[
        [
            "股票代號",
            "股票名稱"
        ]
    ],

    on="股票代號",

    how="left"

)

# ===== 欄位順序 =====

result_df = result_df[
    [
        "股票代號",
        "股票名稱",
        "族群"
    ]
]

# ===== 排序 =====

result_df = result_df.sort_values(

    by=[
        "族群",
        "股票代號"
    ]

)

# ===== 輸出 =====

result_df.to_csv(

    "sector_master.csv",

    index=False,

    encoding="utf-8-sig"

)

print()

print(
    f"族群數量: {result_df['族群'].nunique()}"
)

print(
    f"股票筆數: {len(result_df)}"
)

print()

print(
    "sector_master.csv 已更新"
)