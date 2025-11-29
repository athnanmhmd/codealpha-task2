# CodeAlpha Task 2: Chatbot Application using Streamlit
#  Developer: Janufar Fathima Ashra
import streamlit as st
from chatbot import FAQChatbot
from datetime import datetime

st.set_page_config(page_title="FAQ Chatbot", layout="wide")

bot = FAQChatbot()

# Sidebar controls 
st.sidebar.title("FAQ Chatbot")
st.sidebar.markdown("Use the sidebar to access controls and sample prompts.")
if st.sidebar.button("Clear chat"):
    st.session_state.chat = []


# Initialize chat state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Ensure input_box exists in session state (initialize before widget creation)
if "input_box" not in st.session_state:
    st.session_state["input_box"] = ""

# If a previous run requested clearing the input, do it before the widget is instantiated
if st.session_state.get("clear_input", False):
    st.session_state["input_box"] = ""
    st.session_state["clear_input"] = False

# Light UI CSS
st.markdown("""
<style>
.chat-header { text-align:center; font-size:28px; font-weight:700; margin-bottom:20px; color:#1f2937; }
.chat-subtitle { text-align:center; color:#6b7280; font-size:14px; margin-bottom:20px; }
.user-bubble { background-color:#dbeafe; color:#1e40af; padding:12px 16px; border-radius:12px; margin:12px 0; text-align:right; display:inline-block; max-width:75%; }
.bot-bubble { background-color:#f3f4f6; color:#1f2937; padding:12px 16px; border-radius:12px; margin:12px 0; text-align:left; display:inline-block; max-width:75%; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='chat-header'>🤖 FAQ Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='chat-subtitle'>Ask anything related to AI, ML, Python or the CodeAlpha Internship</div>", unsafe_allow_html=True)

# Modern message rendering with avatars and timestamps
for msg in st.session_state.chat:
        # support both (sender, text) and (sender, text, timestamp)
        if len(msg) == 3:
                sender, text, ts = msg
        else:
                sender, text = msg
                ts = ""

        if sender == "user":
                st.markdown(f"""
                <div style='display:flex; justify-content:flex-end; gap:8px; margin-bottom:8px;'>
                    <div style='max-width:75%; text-align:right;'>
                        <div style='display:inline-block; background:#dbeafe; color:#1e40af; padding:10px 14px; border-radius:12px;'>{text}</div>
                        <div style='font-size:11px; color:#6b7280; margin-top:4px;'>{ts}</div>
                    </div>
                    <div style='width:36px; height:36px; background:#60a5fa; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center;'>🙂</div>
                </div>
                """, unsafe_allow_html=True)
        else:
                st.markdown(f"""
                <div style='display:flex; justify-content:flex-start; gap:8px; margin-bottom:8px;'>
                    <div style='width:36px; height:36px; background:#94a3b8; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center;'>🤖</div>
                    <div style='max-width:75%; text-align:left;'>
                        <div style='display:inline-block; background:#f3f4f6; color:#1f2937; padding:10px 14px; border-radius:12px;'>{text}</div>
                        <div style='font-size:11px; color:#6b7280; margin-top:4px;'>{ts}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Input area
st.write("")
col1, col2 = st.columns([5, 1])
with col1:
    user_msg = st.text_input("", placeholder="Type your message here...", key="input_box", label_visibility="collapsed")
with col2:
    send = st.button("Send", key="send_btn", use_container_width=True)

if send:
    if user_msg and user_msg.strip():
        now = datetime.now().strftime('%H:%M')
        st.session_state.chat.append(("user", user_msg.strip(), now))
        reply = bot.get_answer(user_msg.strip())
        now_bot = datetime.now().strftime('%H:%M')
        st.session_state.chat.append(("bot", reply, now_bot))
        # Mark input to be cleared on next run (must set before widget creation)
        st.session_state["clear_input"] = True
        st.rerun()