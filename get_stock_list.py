import requests
import pandas as pd
import urllib3

# ===== 關閉 SSL 警告 =====

urllib3.disable_warnings()

stock_list = []

# ===== 上市股票 =====

url_twse = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

try:

    data = requests.get(
        url_twse,
        timeout=30
    ).json()

    for row in data:

        try:

            stock_id = str(
                row["Code"]
            )

            stock_name = str(
                row["Name"]
            )

            # ===== 只保留4碼股票 =====

            if len(stock_id) != 4:
                continue

            if not stock_id.isdigit():
                continue

            stock_list.append([

                stock_id,
                stock_name

            ])

        except:
            continue

except Exception as e:

    print("上市股票錯誤:", e)

# ===== 上櫃股票 =====

url_tpex = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes"

try:

    data = requests.get(
        url_tpex,
        timeout=30,
        verify=False
    ).json()

    for row in data:

        try:

            stock_id = str(
                row["SecuritiesCompanyCode"]
            )

            stock_name = str(
                row["CompanyName"]
            )

            # ===== 只保留4碼股票 =====

            if len(stock_id) != 4:
                continue

            if not stock_id.isdigit():
                continue

            stock_list.append([

                stock_id,
                stock_name

            ])

        except:
            continue

except Exception as e:

    print("上櫃股票錯誤:", e)

# ===== DataFrame =====

result_df = pd.DataFrame(

    stock_list,

    columns=[

        "股票代號",
        "股票名稱"

    ]

)

# ===== 去重複 =====

result_df = result_df.drop_duplicates()

# ===== 排序 =====

result_df = result_df.sort_values(
    by="股票代號"
)

# ===== 儲存 =====

result_df.to_csv(

    "stock_list.csv",

    index=False,

    encoding="utf-8-sig"

)

# ===== 顯示 =====

print("\nstock_list.csv 已更新")

print(f"股票數量: {len(result_df)}")