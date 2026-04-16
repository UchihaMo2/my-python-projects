import yfinance as yf

def get_stock_price(symbol):
    try:
        # 建立 Ticker 物件
        stock = yf.Ticker(symbol)
        
        # 獲取最新即時資料 (1天內)
        data = stock.history(period="1d")
        
        if data.empty:
            return f"❌ 找不到股票代號: {symbol}"
        
        # 獲取基本資訊
        info = stock.info
        company_name = info.get('shortName', '未知公司')
        current_price = data['Close'].iloc[-1]
        open_price = data['Open'].iloc[-1]
        
        # 計算漲跌
        change = current_price - open_price
        change_percent = (change / open_price) * 100
        
        color_emoji = "📈" if change >= 0 else "📉"
        
        return (f"{color_emoji} {company_name} ({symbol.upper()})\n"
                f"今日股價: ${current_price:.2f}\n"
                f"今日漲跌: {change:+.2f} ({change_percent:+.2f}%)")

    except Exception as e:
        return f"⚠️ 發生錯誤: {e}"

def main():
    print("=== 美股即時行情查詢 (資料來源: Yahoo Finance) ===")
    ticker_input = input("請輸入美股代號 (例如 AAPL, NVDA, TSLA): ").strip()
    
    if ticker_input:
        print("\n查詢中，請稍候...")
        result = get_stock_price(ticker_input)
        print("-" * 30)
        print(result)
        print("-" * 30)
    else:
        print("請輸入有效的代號。")

if __name__ == "__main__":
    main()
