import os
from typing import List, Dict, Optional, Type

from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_community.tools.jira.prompt import (
    JIRA_JQL_PROMPT,
    JIRA_GET_ALL_PROJECTS_PROMPT,
    JIRA_ISSUE_CREATE_PROMPT,
    JIRA_CATCH_ALL_PROMPT,
    JIRA_CONFLUENCE_PAGE_CREATE_PROMPT,
)
from langchain_community.tools.jira.tool import JiraAction
from langchain_core.pydantic_v1 import BaseModel, Field

llm = ChatOpenAI(temperature=0)

jira = JiraAPIWrapper()


class ProjectParam(BaseModel):
    """Schema for operations that require a Project name as input."""
    key: str = Field(..., description="The name of Jira project.")


class IssueTypeParam(BaseModel):
    """Schema for operations that require an IssueType as input."""
    name: str = Field(..., description="The name of Jira project.")


class CreateIssueParam(BaseModel):
    """Schema for operations that require task summary, project, and issuetype as input."""
    project: ProjectParam
    issuetype: IssueTypeParam
    summary: str = Field(..., description="The description of task.")



class CustomJiraAction(JiraAction):
    arg_schema: Optional[Type[BaseModel]] = None


    def _run(self, project: ProjectParam, issuetype: IssueTypeParam, summary: str) -> str:
        import json
        query_dict = {
            "summary": summary,
            "project": project.dict(),
            "issuetype": issuetype.dict(),
        }
        query = json.dumps(query_dict)
        return self.api_wrapper.issue_create(query)



class CustomJiraToolkit(JiraToolkit):
    """Custom jira toolkit for OpenAI tool calling."""

    @classmethod
    def from_jira_api_wrapper(cls, jira_api_wrapper: JiraAPIWrapper) -> "JiraToolkit":
        operations: List[Dict] = [
            {
                "mode": "jql",
                "name": "jql_query",
                "description": JIRA_JQL_PROMPT,
            },
            # {
            #     "mode": "create_issue",
            #     "name": "create_issue",
            #     "description": JIRA_ISSUE_CREATE_PROMPT,
            # },
            {
                "mode": "get_projects",
                "name": "get_projects",
                "description": JIRA_GET_ALL_PROJECTS_PROMPT,
            },
            {
                "mode": "other",
                "name": "catch_all_api_call",
                "description": JIRA_CATCH_ALL_PROMPT,
            },
            {
                "mode": "create_page",
                "name": "create_confluence_page",
                "description": JIRA_CONFLUENCE_PAGE_CREATE_PROMPT,
            },
        ]
        tools = [
            JiraAction(
                name=action["name"],
                description=action["description"],
                mode=action["mode"],
                api_wrapper=jira_api_wrapper,
            )
            for action in operations
        ]
        tools.append(
            CustomJiraAction(
                mode="create_issue",
                name="create_issue",
                description=JIRA_ISSUE_CREATE_PROMPT,
                args_schema=CreateIssueParam,
            )
        )
        return cls(tools=tools)  # type: ignore[arg-type]

toolkit = CustomJiraToolkit.from_jira_api_wrapper(jira)

prompt = hub.pull("hwchase17/openai-tools-agent")
tools = toolkit.get_tools()

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

answer = agent_executor.invoke(
    {"input": "Please add a JIRA task to remind me to 'make more fried rice.'"})
print(answer["output"])
