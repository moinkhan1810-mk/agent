import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS

# Page Configuration
st.set_page_config(
    page_title="Research AI Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom UI Styling
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
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
st.caption("Powered by CrewAI & Groq")

# Sidebar Configuration
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

# Custom Tool
@tool("DuckDuckGo Web Search")
def web_search_tool(query: str) -> str:
    """Searches the live web using DuckDuckGo and returns top search results."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n")
    return "\n---\n".join(results) if results else "No search results found."

# Main Execution Function
def run_research_crew(topic: str, api_key: str, status_callback=None):
    # Initialize CrewAI native LLM wrapper with Groq
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.3
    )

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Uncover detailed, accurate, and up-to-date facts about topic: {topic}",
        backstory="You are an expert researcher. You excel at searching the web and summarizing complex insights.",
        tools=[web_search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    writer = Agent(
        role="Lead Content Strategist",
        goal=f"Transform raw research findings on {topic} into a structured report",
        backstory="You take detailed analytical reports and translate them into polished, easy-to-read summaries.",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    research_task = Task(
        description=f"Conduct deep research on '{topic}'. Search for latest developments and reliable insights.",
        expected_output="A detailed document containing key facts and developments.",
        agent=researcher
    )

    writing_task = Task(
        description=f"Synthesize the research findings on '{topic}' into a well-structured final report.",
        expected_output="A polished report formatted in Markdown.",
        agent=writer
    )

    def task_callback(task_output):
        if status_callback:
            status_callback(f"Completed step: {task_output.description[:50]}...")

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        task_callback=task_callback,
        verbose=True
    )

    if status_callback:
        status_callback("🕵️ **Senior Research Analyst** is gathering insights...")

    return crew.kickoff(inputs={"topic": topic})

# Main Application Interface
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
            update_ui_status("Initializing Multi-Agent Team...")
            
            with st.spinner("Multi-Agent team working on your topic..."):
                final_output = run_research_crew(
                    topic=topic,
                    api_key=groq_api_key,
                    status_callback=update_ui_status
                )

            status_placeholder.markdown('<div class="status-box" style="border-left-color: #10B981;">✅ <b>Status:</b> Research Completed Successfully!</div>', unsafe_allow_html=True)
            
            st.subheader("📋 Final Research Report")
            st.markdown(final_output)

            st.download_button(
                label="📥 Download Report (.md)",
                data=str(final_output),
                file_name=f"research_{topic.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )

        except Exception as e:
            status_placeholder.empty()
            st.error(f"An error occurred during execution: {str(e)}")
