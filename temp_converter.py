def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def celsius_to_kelvin(c):
    return c + 273.15

def main():
    print("--- 溫度轉換工具 ---")
    print("1. 攝氏 (C) 轉 華氏 (F)")
    print("2. 華氏 (F) 轉 攝氏 (C)")
    print("3. 攝氏 (C) 轉 克耳文 (K)")
    
    choice = input("\n請選擇轉換類型 (1/2/3): ")
    
    try:
        temp = float(input("請輸入要轉換的數值: "))
        
        if choice == '1':
            print(f"結果: {temp}°C = {celsius_to_fahrenheit(temp):.2f}°F")
        elif choice == '2':
            print(f"結果: {temp}°F = {fahrenheit_to_celsius(temp):.2f}°C")
        elif choice == '3':
            print(f"結果: {temp}°C = {celsius_to_kelvin(temp):.2f}K")
        else:
            print("無效的選擇，請輸入 1, 2 或 3。")
            
    except ValueError:
        print("錯誤：請輸入正確的數字格式！")

if __name__ == "__main__":
    main()
