from crewai import Agent
from tools.search_tool import web_search_tool

def create_researcher_agent(llm):
    return Agent(
        role="Senior Research Analyst",
        goal="Uncover detailed, accurate, and up-to-date facts about topic: {topic}",
        backstory="""You are an expert researcher. You excel at searching the web, 
        evaluating sources, collecting evidence, and summarizing complex insights.""",
        tools=[web_search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
