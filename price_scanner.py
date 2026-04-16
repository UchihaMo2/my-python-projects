import streamlit as st
import pytesseract
from PIL import Image
import requests
import re # 用於在文字中尋找數字

# --- 設定 ---
st.title("📷 商品價錢相機換算器")

# 免費匯率 API (不需要 Key)
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/"

# --- 功能函數 ---

def get_exchange_rate(base, target):
    """獲取匯率"""
    try:
        response = requests.get(f"{EXCHANGE_API_URL}{base.upper()}")
        data = response.json()
        if data["result"] == "success":
            return data["rates"].get(target.upper())
    except Exception as e:
        st.error(f"匯率獲取失敗: {e}")
    return None

def extract_price_from_image(image):
    """使用 OCR 從圖片提取數字"""
    # 將圖片轉換為灰階，提高 OCR 準確率
    gray_image = image.convert('L')
    
    # 使用 Tesseract 辨識文字
    # Note: 部署時，這裡需要特別設定 tesseract 的路徑
    text = pytesseract.image_to_string(gray_image)
    
    st.write("### 辨識到的原始文字:")
    st.code(text) # 讓你看看辨識出什麼

    # 使用正規表達式尋找可能的數字 (例如: 12.99, 100)
    # 這個正則非常簡單，實際情況需要更複雜的篩選
    prices = re.findall(r"\d+\.\d+|\d+", text)
    
    if prices:
        # 假設找到的第一個數字就是價格 (這是一個很大的假設)
        return float(prices[0])
    return None

# --- 介面 ---

# 1. 選擇幣值
col1, col2 = st.columns(2)
with col1:
    base_currency = st.selectbox("商品原本幣值", ["USD", "JPY", "EUR", "KRW"], index=0)
with col2:
    target_currency = st.selectbox("換算成", ["TWD", "HKD", "CNY"], index=0)

# 2. 相機輸入
# Streamlit 的 camera_input 元件，在手機上會啟動相機
uploaded_file = st.camera_input("請對準商品價格拍照")

# 3. 處理邏輯
if uploaded_file is not None:
    # 讀取圖片
    image = Image.open(uploaded_file)
    st.image(image, caption='已上傳照片', use_column_width=True)
    
    with st.spinner('正在辨識價格中...'):
        original_price = extract_price_from_image(image)
        
    if original_price is not None:
        st.success(f"成功辨識價格: **{original_price:.2f} {base_currency.upper()}**")
        
        with st.spinner('正在獲取即時匯率...'):
            rate = get_exchange_rate(base_currency, target_currency)
            
        if rate:
            converted_price = original_price * rate
            st.metric(
                label=f"換算為 {target_currency.upper()}",
                value=f"{converted_price:.2f}",
                delta=f"1 {base_currency} = {rate:.4f} {target_currency}"
            )
        else:
            st.error("無法完成換算。")
    else:
        st.warning("無法從圖片中辨識出明確的數字價格。請確保照片清晰且只包含價格。")

