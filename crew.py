from langchain_groq import ChatGroq
from crewai import Task, Crew, Process
from agents.researcher import create_researcher_agent
from agents.writer import create_writer_agent

def run_research_crew(topic: str, groq_api_key: str, status_callback=None):
    # Initialize Groq LLM via LangChain integration for CrewAI
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="groq/llama-3.3-70b-versatile",
        temperature=0.3
    )

    # Initialize Agents
    researcher = create_researcher_agent(llm)
    writer = create_writer_agent(llm)

    # Define Tasks
    research_task = Task(
        description="""Conduct deep research on '{topic}'. Search for latest developments, key takeaways, 
        and reliable insights. Compile comprehensive notes with factual findings.""",
        expected_output="A detailed document containing key facts, developments, and sources regarding {topic}.",
        agent=researcher
    )

    writing_task = Task(
        description="""Synthesize the research findings on '{topic}' into a well-structured final report. 
        Organize into sections: Key Highlights, Deep Dive Analysis, and Conclusion.""",
        expected_output="A polished report formatted in Markdown.",
        agent=writer
    )

    # Callback wrapper for UI updates
    def task_callback(task_output):
        if status_callback:
            status_callback(f"Completed step for task: {task_output.description[:50]}...")

    # Build Crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        task_callback=task_callback,
        verbose=True
    )

    if status_callback:
        status_callback("🕵️ **Senior Research Analyst** is gathering insights...")

    result = crew.kickoff(inputs={"topic": topic})
    return result
