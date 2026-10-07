from langchain.agents import create_agent
from langchain.messages import HumanMessage
from model import openai_model
from tools import search_web
import logging
from langchain.tools import tool

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# creating subagents
logging.info("initializing subagent1....")
subagent1 = create_agent(
    model=openai_model,
    tools=[search_web],
    name="SubAgent1",
    system_prompt="You research wedding venues and catering. Use search_web to find options matching the query "
                  "and return a concise summary with names, location, capacity, prices, availability and source URLs."
)

logging.info("initializing subagent2....")
subagent2 = create_agent(
    model=openai_model,
    tools=[search_web],
    name="SubAgent2",
    system_prompt="You research wedding vendors: photographers, decorators, attire and music. Use search_web to find "
                  "options matching the query and return a concise summary with names, prices, style and source URLs."
)

@tool
def delegate_to_subagent1(query: str)->str:
    """Research wedding venues and catering options (location, capacity, price, availability).
    Pass a specific query including city, budget, guest count and date."""
    logging.info(f"Delegating query to SubAgent1: {query}")
    response = subagent1.invoke({"messages":[HumanMessage(content=query)]})
    return response["messages"][-1].content

@tool
def delegate_to_subagent2(query: str)->str:
    """Research wedding vendors: photographers, decorators, attire, music, with prices.
    Pass a specific query including city, budget and style preferences."""
    logging.info(f"Delegating query to SubAgent2: {query}")
    response = subagent2.invoke({"messages":[HumanMessage(content=query)]})
    return response["messages"][-1].content