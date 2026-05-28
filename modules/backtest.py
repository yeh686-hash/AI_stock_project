import pandas as pd
import random

# ===== 讀取觀察名單 =====

df = pd.read_csv(
    "watchlist.csv"
)

print("\n===== AI回測資料 =====\n")

print(df.head())

print("\n股票數量:", len(df))

# ===== 模擬隔日漲跌 =====

results = []

for _, row in df.iterrows():

    # ===== 模擬隔日漲幅 =====

    next_day = round(
        random.uniform(-5, 8),
        2
    )

    # ===== 勝負 =====

    win = "失敗"

    if next_day > 0:
        win = "成功"

    results.append([

        row["AI等級"],
        row["代號"],
        row["名稱"],
        row["族群"],
        row["分數"],
        next_day,
        win

    ])

# ===== DataFrame =====

result_df = pd.DataFrame(

    results,

    columns=[

        "AI等級",
        "代號",
        "名稱",
        "族群",
        "分數",
        "隔日漲幅",
        "結果"

    ]

)

# ===== 顯示 =====

print("\n===== AI勝率模擬 =====\n")

print(result_df)

# ===== 勝率 =====

win_rate = round(

    len(
        result_df[
            result_df["結果"] == "成功"
        ]
    )
    /
    len(result_df)
    * 100,

    2

)

print(f"\n整體勝率: {win_rate}%")

# ===== S級勝率 =====

s_df = result_df[
    result_df["AI等級"] == "S"
]

if len(s_df) > 0:

    s_win = round(

        len(
            s_df[
                s_df["結果"] == "成功"
            ]
        )
        /
        len(s_df)
        * 100,

        2

    )

    print(f"S級勝率: {s_win}%")