"""Jira agent."""

from __future__ import annotations

import enum

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_openai.chat_models import ChatOpenAI

from aipm.tools import CustomJiraToolkit

llm = ChatOpenAI(temperature=0)
jira = JiraAPIWrapper()

toolkit = CustomJiraToolkit.from_jira_api_wrapper(jira)


class AgentMode(enum.Enum):
    PLANNING = "PLANNING"
    DAILY_SPRINT = "DAILY_SPRINT"


def get_agent(mode: AgentMode, verbose: bool = False):
    prompt = hub.pull("hwchase17/openai-tools-agent")

    if mode is AgentMode.DAILY_SPRINT:
        pass
    else:
        prompt.messages[
            0
        ].prompt.template = """You are an expert project manager.

        Your team consists of two engineers and one designer.
        You must manage a sprint with your teammates.
        At the beginning of the sprint, one of the teammates will inform you the tasks that should be done during the sprint.
        For each task, you have to create a JIRA issue using the `create_issue` tool.
        To create an issue, you must know the following arguments:
        1. summary
        2. project
        3. issuetype

        If one of the required information is missing, please ask, not assuming any default values.
        For the 'project' argument, you can infer it by invoking `get_projects` tool."""

    tools = toolkit.get_tools()

    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=verbose)
