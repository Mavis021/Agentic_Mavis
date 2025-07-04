
from dotenv import load_dotenv

load_dotenv()

import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub


from tools.tools import get_profile_url_tavily

def lookup(name: str) -> str:

    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
    template = """
                    Given the full name {name_of_person}, return the LinkedIn URL of the person. 
                    Your answer should contain only a URL"""
    
    prompt_templete = PromptTemplate(
        template=template,
        input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="Use this tool to lookup a person's LinkedIn URL by their full name."
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, 
                               tools=tools_for_agent, 
                               prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)
    result = agent_executor.invoke(input={"input":prompt_templete.format_prompt(name_of_person=name)})

    linkedin_url = result["output"]

    return linkedin_url


if __name__ == "__main__":
    name = "Elon Musk"
    linkedin_url = lookup(name=name)
    print(f"LinkedIn URL for {name}: {linkedin_url}")