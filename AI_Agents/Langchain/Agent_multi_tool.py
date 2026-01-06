from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

load_dotenv()

## we need the web search tool

@tool("get_current_date_time")
def get_current_date_time() -> str:
    """Get the current date and time in the format YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

search_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(model="gpt-4o")
tools = [get_current_date_time, search_tool]
llm_with_tools = llm.bind_tools(tools=tools)

prompt = PromptTemplate.from_template(
    """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """)
## https://smith.langchain.com/hub/hwchase17/react
### or prompt = client.pull_prompt("hwchase17/react")


agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, llm=llm_with_tools)
## you have to mention tools at both places, otherwise agent_executor wont know those tools are available

def chat(query: str) -> str:
    ## we replace all content with an agent
    result = agent_executor.invoke({"input": query})
    return result["output"]


#response = chat("Current time in the country where Messi's debut match for the club took place on July 21, 2023, in a Leagues Cup game against Cruz Azul")
response = chat("Current time in the country where Messi visited in Dec 2025")
#response = chat("Who is the founder of Coursera?")
print(response)
### Output
"""
    > Entering new AgentExecutor chain...
To answer the question about the current time in the country where Lionel Messi visited in December 2025, I first need to find out which country Messi visited at that time.

Action: duckduckgo_search
Action Input: "Messi visit December 2025 country"
2 weeks ago - Lionel Messi's G.O.A.T. India Tour 2025 is a high-profile promotional and fan engagement tour by Argentine footballer Lionel Messi across India during December 2025. As a celebration of Messi's status among the greatest football players of all time, the tour included public appearances, exhibition matches, community events, and cultural engagements in several major Indian cities. This is Messi's first visit to India since 2011. October 2, 2025 - ... Lionel Messi will return to India this December as part of the GOAT Tour 2025 , with the football legend confirming the trip in an official statement on Thursday. “It is such an honour for me to make this trip. 2 weeks ago - Lionel Messi will arrive in India on Saturday for the GOAT India Tour 2025, which will take the football legend to Kolkata, Hyderabad, Mumbai and New Delhi over three days. The Lionel Messi GOAT India Tour opens on December 13 in Kolkata and ... 3 weeks ago - 17, 2025 ... Lionel Messi’s three-day ‘GOAT Tour’ to India — marred by chaotic scenes inside a stadium and the tour’s promoter being arrested and detained — has come to an end. Messi arrived in India on December 13 to thousands of fans lining the streets to catch a glimpse of who many believe is the greatest footballer of all time, hence the tour being called ‘GOAT’, an acronym of greatest of all time. ... And after visits to Kolkata, Hyderabad, Mumbai and ending his trip in New Delhi, the country’s capital, the Argentine World Cup winner, who was joined by Luis Suarez and Rodrigo De Paul, two of his Inter Miami team-mates, certainly left his mark. 3 weeks ago - Messi shared that it is always an honour to play in a country that has so much passion for football and wrote that he looks forward to meeting the new generation of Indian fans. ... This will be Messi’s second trip to India and it promises to be more than just football. His tour is packed with concerts, charity events and meet-and-greet sessions with some of India’s biggest names. Messi’s India journey will begin in Kolkata on December 13, 2025...Messi visited India in December 2025 during his G.O.A.T. India Tour. Now, to find out the current time in India, I will get the current date and time.       

Action: get_current_date_time
Action Input: None2026-01-06 15:49:31The current date and time I have access to is January 6, 2026, 15:49:31. To determine the current time in India, I need to consider the time zone difference. India is in the Indian Standard Time (IST) zone, which is UTC+5:30.

Since there is no information given about which timezone this current date and time is in, I will assume it is in UTC (Coordinated Universal Time) for calculation purposes:

- UTC time: 2026-01-06 15:49:31
- IST is UTC+5:30, so we add 5 hours 30 minutes to the UTC time.
  
Therefore, the current time in India would be:

- IST time: 2026-01-06 21:19:31

Final Answer: The current time in India is 2026-01-06 21:19:31 IST.

> Finished chain.
The current time in India is 2026-01-06 21:19:31 IST.
"""
