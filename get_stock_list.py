import pandas as pd
import twstock

# ===== 股票資料 =====

stocks = twstock.codes

# ===== 建立清單 =====

data = []

for stock_id in stocks:

    try:

        stock = stocks[stock_id]

        # ===== 過濾股票 =====

        if stock.market not in [

            "上市",
            "上櫃"

        ]:

            continue

        data.append([

            stock.code,
            stock.name

        ])

    except:

        continue

# ===== DataFrame =====

df = pd.DataFrame(

    data,

    columns=[

        "股票代號",
        "股票名稱"

    ]

)

# ===== 存檔 =====

df.to_csv(

    "stock_list.csv",

    index=False,

    encoding="utf-8-sig"

)

print("\n股票清單建立完成")

print(
    f"股票數量: {len(df)}"
)