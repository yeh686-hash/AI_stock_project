import os

print("更新股票資料...")
os.system("python core/update_data.py")

print("\n執行AI選股...")
os.system("python core/main.py")

print("\n分析主流輪動...")
os.system("python modules/sector_rotation.py")

print("\n建立AI觀察名單...")
os.system("python modules/watchlist.py")

print("\n分析市場情緒...")
os.system("python modules/market_sentiment.py")

print("\n執行AI回測...")
os.system("python modules/backtest.py")

print("\n執行真實回測...")
os.system("python modules/real_backtest.py")

print("\n===== AI系統執行完成 =====")