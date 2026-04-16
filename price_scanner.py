import streamlit as st
import pytesseract
from PIL import Image
import requests
import re

# 設定頁面資訊
st.set_page_config(page_title="相機換匯器", page_icon="💰")
st.title("📷 拍照即時換匯")

# 1. 設定匯率 API (使用免金鑰的開放 API)
def get_rate(base, target):
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        res = requests.get(url).json()
        return res['rates'][target]
    except:
        return None

# 2. 介面設定
st.sidebar.header("匯率設定")
base_currency = st.sidebar.selectbox("商品標價幣別", ["JPY", "USD", "EUR", "KRW"], index=0)
target_currency = st.sidebar.selectbox("想換算成", ["TWD", "HKD", "CNY"], index=0)

# 3. 相機啟動
img_file = st.camera_input("請對準標價拍照（請確保數字清晰）")

if img_file:
    # 讀取照片
    image = Image.open(img_file)
    
    # 進行 OCR 辨識
    with st.spinner('偵測數字中...'):
        # 這裡告訴 Tesseract 只偵測數字和點，提高準確率
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        detected_text = pytesseract.image_to_string(image, config=custom_config)
        
        # 使用正則表達式提取數字
        prices = re.findall(r"\d+\.?\d*", detected_text)
    
    if prices:
        # 取得辨識到的第一個數字
        price = float(prices[0])
        st.write(f"### 偵測到價格: {price} {base_currency}")
        
        # 換算匯率
        rate = get_rate(base_currency, target_currency)
        if rate:
            result = price * rate
            st.metric(label=f"換算後 ({target_currency})", value=f"${result:,.2f}")
            st.info(f"今日匯率: 1 {base_currency} = {rate:.4f} {target_currency}")
        else:
            st.error("無法取得即時匯率，請檢查網路。")
    else:
        st.warning("拍謝！我沒看到數字，請再拍近一點或清楚一點。")
        st.write("辨識到的文字內容為:", detected_text) # 偵錯用
