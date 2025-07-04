from typing import Tuple

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from third_parties.linkedin import get_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary

from dotenv import load_dotenv


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = get_linkedin_profile(linkedin_url=linkedin_username, mock=False)

    summary_template = """

    given the Linkedin information {information} about a persion from I want you to create:
    1. a short summary
    2. two interesting facts about them 
    
    use the information from LinkedIn
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    
  #  chain = LLMChain(llm=llm, prompt=summary_prompt_template, output_parser=summary_parser)

    chain = summary_prompt_template | llm | summary_parser
    summary_and_facts = chain.invoke(input={"information": linkedin_data})
    

    if not summary_and_facts.facts:
        summary_and_facts.facts = ["No interesting facts found."]

    if not summary_and_facts.summary:
        summary_and_facts.summary = "No summary found."


    print(f"Summary: {summary_and_facts}")


    return summary_and_facts, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":

    load_dotenv()
    print("Ice Breaker")

    ice_break_with(name="Eden Marco")


