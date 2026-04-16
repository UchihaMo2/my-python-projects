import requests

def get_exchange_rate(base_currency, target_currency):
    """取得即時匯率 (使用定時更新的開放 API)"""
    url = f"https://open.er-api.com/v6/latest/{base_currency.upper()}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["result"] == "success":
            rate = data["rates"].get(target_currency.upper())
            if rate:
                return rate
            else:
                return "找不到目標貨幣"
        else:
            return "API 請求失敗"
            
    except Exception as e:
        return f"發生錯誤: {e}"

def main():
    print("--- 簡易匯率查詢工具 ---")
    base = input("請輸入原始貨幣 (例如 USD): ") or "USD"
    target = input("請輸入目標貨幣 (例如 TWD): ") or "TWD"
    
    rate = get_exchange_rate(base, target)
    
    if isinstance(rate, float):
        print(f"目前的匯率為: 1 {base.upper()} = {rate:.2f} {target.upper()}")
    else:
        print(f"錯誤: {rate}")

if __name__ == "__main__":
    main()
