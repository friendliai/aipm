"""Jira tools."""

from __future__ import annotations

from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.tools.jira.prompt import (
    JIRA_GET_ALL_PROJECTS_PROMPT,
    JIRA_ISSUE_CREATE_PROMPT,
    JIRA_JQL_PROMPT,
)
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_core.pydantic_v1 import BaseModel

from aipm.actions import (
    CreateIssueJiraAction,
    GetIssueTransitionsAction,
    GetProjectsJiraAction,
    IssueTransitionAction,
    JqlJiraAction,
)
from aipm.params import (
    CreateIssueParam,
    GetIssueTransitionsParam,
    IssueTransitionParam,
    JqlParam,
)
from aipm.prompts import (
    JIRA_GET_ISSUE_TRANSITIONS_PROMPT,
    JIRA_ISSUE_TRANSITIONS_PROMPT,
)


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
            IssueTransitionAction(
                mode="issue_transition",
                name="issue_transition",
                description=JIRA_ISSUE_TRANSITIONS_PROMPT,
                args_schema=IssueTransitionParam,
            ),
            GetIssueTransitionsAction(
                mode="get_issue_transitions",
                name="get_issue_transitions",
                description=JIRA_GET_ISSUE_TRANSITIONS_PROMPT,
                args_schema=GetIssueTransitionsParam,
            ),
        ]
        return cls(tools=tools)  # type: ignore[arg-type]
