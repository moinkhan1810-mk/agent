import streamlit as st
import os
from crew import run_research_crew

# Page configuration
st.set_page_config(
    page_title="Research AI Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Modern Dark Aesthetic)
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .stAppHeader {
        background-color: rgba(0,0,0,0);
    }
    .agent-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .status-box {
        padding: 12px 18px;
        border-radius: 10px;
        background: #1E2640;
        border-left: 4px solid #6366F1;
        color: #E2E8F0;
        font-weight: 500;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ AI Research Multi-Agent Team")
st.caption("Powered by CrewAI & Groq (Llama 3.3 70B)")

# Sidebar Settings
with st.sidebar:
    st.header("🔑 Credentials")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Get key from console.groq.com")
    
    st.divider()
    st.header("🤖 Active Crew")
    st.markdown("""
    <div class="agent-card">
        <b>🕵️ Senior Research Analyst</b><br/>
        <small>Scours the live web using DDG search tools.</small>
    </div>
    <div class="agent-card">
        <b>✍️ Lead Content Strategist</b><br/>
        <small>Structures analytical findings into clear reports.</small>
    </div>
    """, unsafe_allow_html=True)

# Main UI layout
topic = st.text_input("Research Topic / Goal", placeholder="e.g., Quantum Computing innovations in 2026")

if st.button("🚀 Launch Research", use_container_width=True, type="primary"):
    if not groq_api_key:
        st.error("Please provide a valid Groq API Key in the sidebar.")
    elif not topic.strip():
        st.warning("Please enter a research topic to proceed.")
    else:
        status_placeholder = st.empty()
        
        def update_ui_status(message: str):
            status_placeholder.markdown(f'<div class="status-box">🔄 <b>Current Stage:</b> {message}</div>', unsafe_allow_html=True)

        try:
            update_ui_status("Initializing Agents & Workflow...")
            
            with st.spinner("Multi-Agent team working on your topic..."):
                final_output = run_research_crew(
                    topic=topic,
                   groq_api_key=groq_api_key,
                    
                    status_callback=update_ui_status
                )

            status_placeholder.markdown('<div class="status-box" style="border-left-color: #10B981;">✅ <b>Status:</b> Research Completed Successfully!</div>', unsafe_allow_html=True)
            
            st.subheader("📋 Final Research Report")
            st.markdown(final_output)

            # Option to download report
            st.download_button(
                label="📥 Download Report (.md)",
                data=str(final_output),
                file_name=f"research_{topic.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )

        except Exception as e:
            status_placeholder.empty()
            st.error(f"An error occurred during execution: {str(e)}")
