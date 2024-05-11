from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI

with open('key.txt', 'r') as file:
    text = file.read()

agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", api_key=text),
    "autos_clean.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

agent.run("Hola buenos días! que autos tiene disponible a un precio barato?")