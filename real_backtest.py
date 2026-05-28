import pandas as pd

# ===== 讀取每日選股 =====

df = pd.read_csv(
    "daily_picks.csv"
)

print("\n===== 真實回測系統 =====\n")

# ===== 日期 =====

dates = sorted(
    df["日期"].unique()
)

# ===== 至少需要兩天 =====

if len(dates) < 2:

    print("歷史資料不足")

    exit()

today = dates[-1]

yesterday = dates[-2]

print(f"今日: {today}")

print(f"昨日: {yesterday}")

# ===== 昨日選股 =====

yesterday_df = df[
    df["日期"] == yesterday
]

# ===== 今日資料 =====

today_df = df[
    df["日期"] == today
]

# ===== 今日價格字典 =====

today_map = {}

for _, row in today_df.iterrows():

    today_map[
        str(row["代號"])
    ] = row["收盤價"]

# ===== 回測 =====

results = []

for _, row in yesterday_df.iterrows():

    stock_id = str(row["代號"])

    old_price = row["收盤價"]

    new_price = today_map.get(
        stock_id,
        None
    )

    # ===== 沒資料 =====

    if new_price is None:
        continue

    # ===== 漲跌幅 =====

    change = round(

        (
            new_price
            -
            old_price
        )
        /
        old_price
        * 100,

        2

    )

    # ===== 勝負 =====

    result = "失敗"

    if change > 0:
        result = "成功"

    results.append([

        stock_id,
        row["名稱"],
        row["族群"],
        row["分數"],
        old_price,
        new_price,
        change,
        result

    ])

# ===== DataFrame =====

result_df = pd.DataFrame(

    results,

    columns=[

        "代號",
        "名稱",
        "族群",
        "分數",
        "昨日收盤",
        "今日收盤",
        "報酬率",
        "結果"

    ]

)

print("\n===== 真實回測結果 =====\n")

print(result_df)

# ===== 勝率 =====

if len(result_df) > 0:

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