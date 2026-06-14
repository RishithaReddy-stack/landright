import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.copilot_agent import ask
from backend.knowledge.content import KNOWLEDGE_BASE

st.set_page_config(
    page_title="LandRight",
    page_icon="🛬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0a0f; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem;
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c084fc, #fb7185);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    animation: fadeInDown 0.8s ease;
}
.hero-sub {
    font-size: 1.1rem;
    color: #94a3b8;
    animation: fadeInUp 0.8s ease;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(129,140,248,0.4); }
    50%       { box-shadow: 0 0 0 8px rgba(129,140,248,0); }
}
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-10px); }
    to   { opacity: 1; transform: translateX(0); }
}

.stage-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin: 1.5rem 0;
}
.stage-pill {
    background: #13131f;
    border: 1px solid #2e2e4a;
    border-radius: 40px;
    padding: 0.6rem 1rem;
    text-align: center;
    cursor: pointer;
    font-size: 0.8rem;
    color: #94a3b8;
    transition: all 0.2s ease;
    animation: fadeInUp 0.5s ease;
}
.stage-pill:hover {
    border-color: #818cf8;
    color: #818cf8;
    transform: translateY(-2px);
}
.stage-pill.active {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    border-color: transparent;
    color: white;
    animation: pulse 2s infinite;
}

.task-card {
    background: #13131f;
    border: 1px solid #2e2e4a;
    border-radius: 16px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.6rem;
    cursor: pointer;
    transition: all 0.2s ease;
    animation: slideIn 0.3s ease;
}
.task-card:hover {
    border-color: #818cf8;
    transform: translateX(4px);
    background: #16162a;
}
.task-title { font-size: 0.95rem; font-weight: 600; color: #e2e8f0; margin-bottom: 4px; }
.task-tag {
    display: inline-block;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 20px;
    background: #1e1e3a;
    color: #818cf8;
    border: 1px solid #3730a3;
}

.chat-wrap {
    background: #13131f;
    border: 1px solid #2e2e4a;
    border-radius: 20px;
    padding: 1.25rem;
    height: 460px;
    overflow-y: auto;
}
.msg-user {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 18px 18px 4px 18px;
    margin: 0.5rem 0 0.5rem 20%;
    font-size: 0.9rem;
    animation: fadeInUp 0.3s ease;
}
.msg-ai {
    background: #1e1e2e;
    color: #e2e8f0;
    padding: 0.75rem 1rem;
    border-radius: 18px 18px 18px 4px;
    margin: 0.5rem 20% 0.5rem 0;
    font-size: 0.9rem;
    border: 1px solid #2e2e4a;
    animation: fadeInUp 0.3s ease;
    line-height: 1.6;
}
.msg-welcome {
    background: linear-gradient(135deg, #1e1b4b, #2d1b69);
    color: #c4b5fd;
    padding: 1rem 1.25rem;
    border-radius: 18px;
    margin-bottom: 1rem;
    border: 1px solid #4c1d95;
    font-size: 0.9rem;
    line-height: 1.7;
}

.divider {
    border: none;
    border-top: 1px solid #2e2e4a;
    margin: 1.5rem 0;
}

.stTextInput input {
    background: #13131f !important;
    border: 1px solid #2e2e4a !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput input:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.15) !important;
}
.stButton button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(79,70,229,0.4) !important;
}

.progress-bar-wrap {
    background: #1e1e2e;
    border-radius: 20px;
    height: 6px;
    margin: 0.5rem 0 1.5rem;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    transition: width 0.5s ease;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_stage" not in st.session_state:
    st.session_state.selected_stage = None
if "expanded_item" not in st.session_state:
    st.session_state.expanded_item = None

st.markdown("""
<div class="hero">
    <div class="hero-title">LandRight 🛬</div>
    <div class="hero-sub">Your AI copilot for landing in the US — built by an international student, for international students.</div>
</div>
""", unsafe_allow_html=True)

stages = {
    "✈️ Pre-arrival": "pre_arrival",
    "🛬 Day 0": "day_0",
    "📅 Week 1": "week_1",
    "📆 Month 1": "month_1",
    "🔄 Ongoing": "ongoing"
}

cols = st.columns(5)
for i, (label, key) in enumerate(stages.items()):
    with cols[i]:
        if st.button(label, key=f"stage_{key}", use_container_width=True):
            st.session_state.selected_stage = key
            st.session_state.expanded_item = None

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

left, right = st.columns([1, 1.4])

with left:
    if st.session_state.selected_stage:
        stage = st.session_state.selected_stage
        stage_label = [k for k, v in stages.items() if v == stage][0]
        st.markdown(f"#### {stage_label}")

        stage_items = [i for i in KNOWLEDGE_BASE if i["category"] == stage]
        total = len(stage_items)

        st.markdown(f"""
        <div class="progress-bar-wrap">
            <div class="progress-bar-fill" style="width: 0%"></div>
        </div>
        """, unsafe_allow_html=True)

        for item in stage_items:
            with st.expander(item["title"]):
                st.markdown(item["content"])
                if st.button("Ask LandRight about this ↗", key=f"ask_{item['id']}"):
                    question = f"Tell me more about: {item['title']}"
                    st.session_state.messages.append({"role": "user", "content": question})
                    with st.spinner("Thinking..."):
                        answer = ask(question, stage=stage)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; padding: 3rem 1rem; color: #4a4a6a;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👆</div>
            <div style="font-size: 1rem; color: #64748b;">Pick a stage above to see your personalised checklist</div>
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("#### Chat with LandRight 💬")

    chat_html = '<div class="chat-wrap" id="chat">'
    if not st.session_state.messages:
        chat_html += """
        <div class="msg-welcome">
            Hey! 👋 I'm LandRight — your AI guide for navigating life in the US as an international student.<br><br>
            Not sure where to start? Click a stage above or just ask me anything —
            banking without SSN, state ID, taxes, OPT, CPT, housing scams... I got you. 🙌
        </div>
        """
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f'<div class="msg-user">{msg["content"]}</div>'
        else:
            chat_html += f'<div class="msg-ai">{msg["content"]}</div>'
    chat_html += '</div>'

    st.markdown(chat_html, unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        cols_input = st.columns([5, 1])
        with cols_input[0]:
            user_input = st.text_input(
                "msg",
                placeholder="e.g. how do I open a bank account without SSN?",
                label_visibility="collapsed"
            )
        with cols_input[1]:
            submitted = st.form_submit_button("Send ↗", use_container_width=True)

        if submitted and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                answer = ask(user_input, stage=st.session_state.selected_stage)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()