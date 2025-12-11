import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 1. 載入設定
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. 設定頁面 (模擬車載寬螢幕)
st.set_page_config(
    page_title="CarSoul AI Cockpit",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. 定義你的專家靈魂 (System Prompt)
SYSTEM_PROMPT = """
You are CarSoul, an empathetic, witty, and highly observant AI driving companion.
Your goal is to keep the driver safe by managing their emotional state.
Tone: Warm, Professional yet Friendly (like Jarvis meets a therapist).
Constraint: Keep responses short (under 2 sentences) because the user is driving.
If the user is angry, use humor to de-escalate.
If the user is tired, ask engaging questions.
"""

# 4. 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# 5. UI 設計：車載儀表板風格
# 自訂 CSS 讓介面變黑，字體變大，隱藏不必要的元素
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        padding: 10px;
    }
    /* 隱藏 Streamlit 預設選單 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 6. 標題區 (可以放你用 Midjourney 生成的 Logo)
col1, col2 = st.columns([1, 5])
with col1:
    # 這裡之後換成 st.image("logo.png")
    st.markdown("# 🚗") 
with col2:
    st.markdown("# CarSoul AI Copilot")
st.markdown("---")

# 7. Demo 快速按鈕 (Demo 神器：避免現場打字手抖)
st.subheader("駕駛情境模擬 (Demo Mode)")
col_demo1, col_demo2, col_demo3 = st.columns(3)

def send_scenario(text):
    st.session_state.messages.append({"role": "user", "content": text})
    
if col_demo1.button("😡 模擬：路怒症發作"):
    send_scenario("前面那台車是不會開車嗎？擋什麼路！開超慢的！")
if col_demo2.button("😴 模擬：長途駕駛疲勞"):
    send_scenario("唉...還要開多久...我好想睡覺...")
if col_demo3.button("😢 模擬：工作受挫"):
    send_scenario("今天老闆罵了我一頓，覺得心情很差，不想回家。")

# 8. 顯示對話歷史
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# 9. 處理使用者輸入與 AI 回應
if prompt := st.chat_input("請輸入指令或是與 CarSoul 對話..."):
    # 顯示使用者輸入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 呼叫 AI (GPT-4o or 3.5)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o", # 或 gpt-3.5-turbo
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # 記錄 AI 回應
    st.session_state.messages.append({"role": "assistant", "content": response})
