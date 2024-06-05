"""Jira agent."""

import typer
from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_core.messages import AIMessage, HumanMessage
from tools import CustomJiraToolkit

llm = ChatOpenAI(temperature=0)
jira = JiraAPIWrapper()

toolkit = CustomJiraToolkit.from_jira_api_wrapper(jira)

prompt = hub.pull("hwchase17/openai-tools-agent")
# 1. summary of the issue
# 2. description of the issue
# 3. assignee of the issue
# 4. due date of the issue
# 5. priority of the issue
# 6. project key

prompt.messages[0].prompt.template = """You are an expert project manager.

Your team consists of two engineers and one designer.
You must manage a sprint with your teammates.
At the beginning of the sprint, one of the teammates will inform you the tasks that should be done during the sprint.
For each task, you have to create a JIRA issue using the `create_issue` tool.
To create an issue, you must know the following arguments:
1. summary
2. project
3. issuetype

If one of the required information is missing, please ask, not assuming any default values.
For the 'project' argument, you can infer it by invoking `get_projects` tool.

Once the tasks are registered, each teammate is going to report his/her daily progress.
You then should provide a summary of daily sprint meeting."""

tools = toolkit.get_tools()

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

history = []
while True:
    user_input = typer.prompt("USER INPUT: ")
    answer = agent_executor.invoke({"input": user_input, "chat_history": history})
    typer.secho(f"AGENT: {answer['output']}", fg=typer.colors.GREEN)
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=answer["output"]))
