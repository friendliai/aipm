"""Jira tools."""

from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.tools.jira.prompt import (
    JIRA_JQL_PROMPT,
    JIRA_GET_ALL_PROJECTS_PROMPT,
    JIRA_ISSUE_CREATE_PROMPT,
)
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_core.pydantic_v1 import BaseModel

from actions import CreateIssueJiraAction, GetProjectsJiraAction, JqlJiraAction
from params import CreateIssueParam, JqlParam


class CustomJiraToolkit(JiraToolkit):
    """Custom jira toolkit for OpenAI tool calling."""

    @classmethod
    def from_jira_api_wrapper(cls, jira_api_wrapper: JiraAPIWrapper) -> JiraToolkit:
        tools = [
            JqlJiraAction(
                mode="jql",
                name="jql_query",
                description=JIRA_JQL_PROMPT,
                args_schema=JqlParam,
            ),
            CreateIssueJiraAction(
                mode="create_issue",
                name="create_issue",
                description=JIRA_ISSUE_CREATE_PROMPT,
                args_schema=CreateIssueParam,
            ),
            GetProjectsJiraAction(
                mode="get_projects",
                name="get_projects",
                description=JIRA_GET_ALL_PROJECTS_PROMPT,
                args_schema=BaseModel,
            ),
        ]
        return cls(tools=tools)  # type: ignore[arg-type]
