"""Jira agent."""

from __future__ import annotations

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai.chat_models import ChatOpenAI

from aipm.api_wrapper import CustomJiraAPIWrapper
from aipm.enum import AgentMode
from aipm.prompt import DAILY_STANDUP_SYSTEM_PROMPT, PLANNING_SYSTEM_PROMPT
from aipm.toolkit import CustomJiraToolkit

llm = ChatOpenAI(temperature=0)
jira = CustomJiraAPIWrapper()

toolkit = CustomJiraToolkit.from_jira_api_wrapper(jira)


PROMPT_TEMPLATE_MAP = {
    AgentMode.PLANNING: PLANNING_SYSTEM_PROMPT,
    AgentMode.STANDUP: DAILY_STANDUP_SYSTEM_PROMPT,
}


def get_agent(mode: AgentMode, verbose: bool = False) -> AgentExecutor:
    prompt = hub.pull("hwchase17/openai-tools-agent")

    try:
        prompt.messages[0].prompt.template = PROMPT_TEMPLATE_MAP[mode]
    except KeyError as e:
        raise ValueError("Invalid agent mode is provided.") from e

    tools = toolkit.get_tools()

    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=verbose)
