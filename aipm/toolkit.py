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

from aipm.tools.jira import (
    CreateIssueJiraTool,
    CreatePageTool,
    GetIssueTransitionsTool,
    GetProjectsJiraTool,
    IssueTransitionTool,
    JqlJiraTool,
)
from aipm.param import (
    CreateIssueParam,
    CreatePageParam,
    GetIssueTransitionsParam,
    IssueTransitionParam,
    JqlParam,
)
from aipm.prompt import (
    CONFLUENCE_CREATE_ISSUE_PROMPT,
    JIRA_GET_ISSUE_TRANSITIONS_PROMPT,
    JIRA_ISSUE_TRANSITIONS_PROMPT,
)


class CustomJiraToolkit(JiraToolkit):
    """Custom jira toolkit for OpenAI tool calling."""

    @classmethod
    def from_jira_api_wrapper(cls, jira_api_wrapper: JiraAPIWrapper) -> JiraToolkit:
        tools = [
            JqlJiraTool(
                mode="jql",
                name="jql_query",
                description=JIRA_JQL_PROMPT,
                args_schema=JqlParam,
            ),
            CreateIssueJiraTool(
                mode="create_issue",
                name="create_issue",
                description=JIRA_ISSUE_CREATE_PROMPT,
                args_schema=CreateIssueParam,
            ),
            GetProjectsJiraTool(
                mode="get_projects",
                name="get_projects",
                description=JIRA_GET_ALL_PROJECTS_PROMPT,
                args_schema=BaseModel,
            ),
            IssueTransitionTool(
                mode="issue_transition",
                name="issue_transition",
                description=JIRA_ISSUE_TRANSITIONS_PROMPT,
                args_schema=IssueTransitionParam,
            ),
            GetIssueTransitionsTool(
                mode="get_issue_transitions",
                name="get_issue_transitions",
                description=JIRA_GET_ISSUE_TRANSITIONS_PROMPT,
                args_schema=GetIssueTransitionsParam,
            ),
            CreatePageTool(
                mode="create_page",
                name="create_page",
                description=CONFLUENCE_CREATE_ISSUE_PROMPT,
                args_schema=CreatePageParam,
            )
        ]
        return cls(tools=tools)  # type: ignore[arg-type]
