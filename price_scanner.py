import streamlit as st
import pytesseract
from PIL import Image
import requests
import re

# --- 頁面設定 ---
st.set_page_config(page_title="相機掃描換匯器", page_icon="💰")
st.title("📷 拍照即時換匯")
st.caption("支援 TWD, CNY, KRW, JPY, USD 等多國幣別")

# --- 1. 匯率獲取函數 ---
@st.cache_data(ttl=3600) # 快取匯率資料一小時，避免重複請求
def get_rate(base, target):
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        res = requests.get(url).json()
        if res['result'] == 'success':
            return res['rates'][target]
        return None
    except:
        return None

# --- 2. 介面設定 (Sidebar) ---
st.sidebar.header("匯率設定")

# 定義支援的幣別清單
currency_list = ["TWD", "CNY", "KRW", "JPY", "USD", "EUR", "HKD"]

# 設定標價幣別 (預設 KRW 為 index 2)
base_currency = st.sidebar.selectbox(
    "商品標價幣別", 
    currency_list, 
    index=currency_list.index("KRW")
)

# 設定換算幣別 (預設 TWD 為 index 0)
target_currency = st.sidebar.selectbox(
    "想換算成", 
    currency_list, 
    index=currency_list.index("TWD")
)

st.sidebar.divider()
st.sidebar.info(f"當前模式: {base_currency} ➡ {target_currency}")

# --- 3. 相機輸入元件 ---
img_file = st.camera_input("請對準商品標價拍照")

if img_file:
    # 讀取圖片
    image = Image.open(img_file)
    
    # 顯示處理中的狀態
    with st.spinner('正在辨識數字中...'):
        # OCR 設定：只偵測數字與小數點
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        detected_text = pytesseract.image_to_string(image, config=custom_config)
        
        # 使用正則表達式提取數字（包含整數或浮點數）
        prices = re.findall(r"\d+\.?\d*", detected_text)
    
    if prices:
        # 取得辨識到的第一個有效數字
        try:
            price = float(prices[0])
            st.write(f"### 🔍 偵測到價格: {price:,.2f} {base_currency}")
            
            # 獲取並計算匯率
            with st.spinner('取得即時匯率中...'):
                rate = get_rate(base_currency, target_currency)
                
            if rate:
                result = price * rate
                # 顯示大大的換算結果
                st.balloons() # 成功的特效
                st.metric(
                    label=f"換算結果 ({target_currency})", 
                    value=f"${result:,.2f}",
                    delta=f"1 {base_currency} = {rate:.4f} {target_currency}"
                )
            else:
                st.error("無法取得匯率，請檢查網路連線。")
                
        except ValueError:
            st.error("數字轉換錯誤。")
    else:
        st.warning("⚠️ 未能辨識到數字。請嘗試近距離拍攝，並確保光線充足。")
        with st.expander("查看辨識結果"):
            st.write(f"OCR 原始文字: {detected_text}")

# --- 4. 使用說明 ---
with st.expander("使用小撇步"):
    st.write("""
    1. **保持對焦**：確保標價數字在畫面中央。
    2. **減少干擾**：盡量不要拍到多組數字，以免程式判斷錯誤。
    3. **光線**：避免反光，這會影響 OCR 的準確率。
    """)
