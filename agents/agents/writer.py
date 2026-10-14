from crewai import Agent

def create_writer_agent(llm):
    return Agent(
        role="Lead Content Strategist",
        goal="Transform raw research findings on {topic} into a highly engaging, structured report",
        backstory="""You are a seasoned editor and technical writer. You take detailed analytical reports 
        and translate them into polished, easy-to-read, beautifully formatted summaries.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
