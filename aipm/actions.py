"""Agent actions."""

from __future__ import annotations

import json
from abc import abstractmethod
from typing import Any, Optional, Type

from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from aipm.api_wrapper import CustomJiraAPIWrapper
from aipm.params import IssueTypeParam, ProjectParam


class JiraAction(BaseTool):
    """Tool that queries the Atlassian Jira API."""

    api_wrapper: JiraAPIWrapper = Field(default_factory=CustomJiraAPIWrapper)  # type: ignore[arg-type]
    mode: str
    name: str = ""
    description: str = ""
    arg_schema: Optional[Type[BaseModel]] = None

    @abstractmethod
    def _run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any: ...


class JqlJiraAction(JiraAction):
    """JQL Jira action."""

    def _run(self, query: str) -> str:
        return self.api_wrapper.search(query)


class CreateIssueJiraAction(JiraAction):
    """Action to create a new issue."""

    def _run(
        self, project: ProjectParam, issuetype: IssueTypeParam, summary: str
    ) -> str:
        query_dict = {
            "summary": summary,
            "project": project.dict(),
            "issuetype": issuetype.dict(),
        }
        query = json.dumps(query_dict)
        return self.api_wrapper.issue_create(query)


class GetProjectsJiraAction(JiraAction):
    """Action to get Jira projects."""

    def _run(self) -> str:
        return self.api_wrapper.project()


class IssueTransitionAction(JiraAction):
    """Action to post Jira issue transition."""

    def _run(self, issue_key: str, status_name: str) -> str:
        query_dict = {"issue_key": issue_key, "status_name": status_name}
        query = json.dumps(query_dict)
        return self.api_wrapper.issue_transition(query)
