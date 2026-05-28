import pandas as pd
from datetime import datetime
import os

# ===== 讀取今日選股 =====

today_df = pd.read_csv(
    "選股結果.csv"
)

# ===== 新增日期 =====

today_df["日期"] = datetime.today().strftime(
    "%Y-%m-%d"
)

# ===== 只保留重要欄位 =====

save_df = today_df[

    [

        "日期",
        "股票代號",
        "股票名稱",
        "族群",
        "分數",
        "5日漲幅",
        "RSI"

    ]

]

# ===== 紀錄檔 =====

record_file = "績效追蹤.csv"

# ===== 如果不存在 =====

if not os.path.exists(record_file):

    save_df.to_csv(

        record_file,

        index=False,

        encoding="utf-8-sig"

    )

    print("已建立績效追蹤檔")

# ===== 已存在 =====

else:

    old_df = pd.read_csv(
        record_file
    )

    combined_df = pd.concat(

        [

            old_df,
            save_df

        ],

        ignore_index=True

    )

    combined_df.to_csv(

        record_file,

        index=False,

        encoding="utf-8-sig"

    )

    print("已更新績效追蹤檔")