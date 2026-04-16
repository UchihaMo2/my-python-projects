import openai

class HRInterviewAgent:
    def __init__(self, candidate_name, job_title, jd_requirements):
        self.client = openai.OpenAI()
        self.candidate_name = candidate_name
        self.job_title = job_title
        # 核心：定義面試官的「人格技能」與「行為準則」
        self.system_prompt = f"""
        # Role
        你是一位在科技業擁有 15 年經驗的資深 HR 與技術面試官。現在你要面試 {candidate_name}，應徵職位是 {job_title}。
        
        # Job Requirements (JD)
        {jd_requirements}

        # Behavioral Rules
        1. **追問到底**：如果候選人的回答過於籠統（例如：我負責過數據優化），你必須追問具體技術細節（例如：用了什麼索引？優化了多少比例？）。
        2. **一次一問**：為了語音體驗，每次只提問一個問題，不要給長篇大論。
        3. **評分導向**：在對話過程中，暗中觀察候選人的邏輯、誠實度與技術深度。
        4. **節奏控制**：如果候選人離題，委婉地將話題拉回技術領域。
        """
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def chat(self, user_input):
        # 1. 記錄候選人的話
        self.messages.append({"role": "user", "content": user_input})
        
        # 2. 呼叫大腦進行推理
        response = self.client.chat.completions.create(
            model="gpt-4o",  # 使用最強模型確保推理邏輯
            messages=self.messages,
            temperature=0.7,
            max_tokens=300
        )
        
        ai_reply = response.choices[0].message.content
        
        # 3. 記錄面試官的話
        self.messages.append({"role": "assistant", "content": ai_reply})
        return ai_reply

# --- 執行 Demo ---
jd = "需精通 Python 分散式架構、有處理過日均千萬級流量經驗、熟悉 Redis 鎖機制。"
bot = HRInterviewAgent("張小明", "後端架構師", jd)

print("--- 面試開始 ---")
print(f"AI 面試官: {bot.chat('你好，我是張小明，來面試架構師職位。')}")

while True:
    u_input = input("候選人: ")
    if u_input.lower() in ['quit', 'exit', '結束']: break
    print(f"AI 面試官: {bot.chat(u_input)}")
