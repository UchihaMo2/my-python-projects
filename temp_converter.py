import streamlit as st

# 設定網頁標題
st.title("🌡️ 溫度轉換工具")

# 定義轉換邏輯
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def celsius_to_kelvin(c):
    return c + 273.15

# Streamlit 介面設計
choice = st.selectbox(
    "請選擇轉換類型",
    ("攝氏 (C) 轉 華氏 (F)", "華氏 (F) 轉 攝氏 (C)", "攝氏 (C) 轉 克耳文 (K)")
)

temp = st.number_input("請輸入要轉換的數值", value=0.0)

if st.button("開始轉換"):
    if choice == "攝氏 (C) 轉 華氏 (F)":
        result = celsius_to_fahrenheit(temp)
        st.success(f"結果: {temp}°C = {result:.2f}°F")
        
    elif choice == "華氏 (F) 轉 攝氏 (C)":
        result = fahrenheit_to_celsius(temp)
        st.success(f"結果: {temp}°F = {result:.2f}°C")
        
    elif choice == "攝氏 (C) 轉 克耳文 (K)":
        result = celsius_to_kelvin(temp)
        st.success(f"結果: {temp}°C = {result:.2f}K")
