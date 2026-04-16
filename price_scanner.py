import streamlit as st
import pytesseract
from PIL import Image
import requests
import re

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="相機掃描換匯器", page_icon="💰", layout="centered")

# 使用自定義 CSS 讓介面在手機上更美觀
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📷 拍照即時換匯")
st.caption("支援 TWD, CNY, KRW, JPY, USD 等多國幣別")

# --- 2. 匯率獲取函數 (帶快取功能) ---
@st.cache_data(ttl=3600)
def get_rate(base, target):
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        res = requests.get(url, timeout=5).json()
        if res['result'] == 'success':
            return res['rates'][target]
        return None
    except Exception:
        return None

# --- 3. 介面設定 (選單) ---
st.sidebar.header("⚙️ 匯率設定")

# 幣別清單
currency_list = ["TWD", "CNY", "KRW", "JPY", "USD", "EUR", "HKD", "GBP"]

# 設定標價幣別 (預設 KRW)
base_currency = st.sidebar.selectbox(
    "1. 商品標價幣別 (原始)", 
    currency_list, 
    index=currency_list.index("KRW")
)

# 設定目標幣別 (預設 TWD)
target_currency = st.sidebar.selectbox(
    "2. 想換算成 (目標)", 
    currency_list, 
    index=currency_list.index("TWD")
)

st.sidebar.divider()
st.sidebar.markdown(f"**目前設定：**\n{base_currency} ➡ {target_currency}")

# --- 4. 相機功能 ---
# 注意：Streamlit 的 camera_input 在手機上會自動彈出系統相機選擇
# 通常會預設為背面鏡頭。若要切換，請使用手機相機介面上的切換按鈕。
img_file = st.camera_input("請對準標價拍照")

if img_file:
    # 讀取並處理圖片
    image = Image.open(img_file)
    
    with st.spinner('🔍 正在辨識價格數字...'):
        # OCR 設定：限制只辨識數字與小數點，提高準確率
        # --psm 6 表示假設圖片為單一均勻的文字區塊
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        detected_text = pytesseract.image_to_string(image, config=custom_config)
        
        # 使用正規表達式抓取數字
        prices = re.findall(r"\d+\.?\d*", detected_text)
    
    if prices:
        try:
            # 取得第一個辨識到的數字
            price = float(prices[0])
            st.markdown(f"### 🎯 偵測到價格：**{price:,.2f} {base_currency}**")
            
            # 取得匯率並計算
            rate = get_rate(base_currency, target_currency)
            
            if rate:
                converted_price = price * rate
                st.divider()
                
                # 顯示核心結果
                st.metric(
                    label=f"換算結果 ({target_currency})", 
                    value=f"${converted_price:,.2f}",
                    delta=f"1 {base_currency} = {rate:.4f} {target_currency}"
                )
                
                # 若成功換算，給一點小特效
                if converted_price > 0:
                    st.toast(f"成功換算！匯率為 {rate}", icon='✅')
            else:
                st.error("❌ 無法取得即時匯率，請檢查網路。")
        except ValueError:
            st.error("❌ 數字處理發生錯誤。")
    else:
        st.warning("⚠️ 沒看到數字喔！請靠近一點拍，並確保畫面只有標價數字。")
        with st.expander("查看掃描到的文字（偵錯用）"):
            st.write(detected_text if detected_text.strip() else "完全沒偵測到文字")

# --- 5. 底部說明 ---
st.divider()
st.info("💡 **小提醒：** 在手機上拍照時，若要換鏡頭，請點擊相機畫面中的反轉圖示。")
