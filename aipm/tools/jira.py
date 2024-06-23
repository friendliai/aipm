"""Jira tool."""

from __future__ import annotations

import json
from abc import abstractmethod
from typing import Any, Optional, Type

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from aipm.api_wrapper import AtlassianAPIWrapper
from aipm.param import IssueParam, IssueTypeParam, ProjectParam, TransitionParam


class JiraTool(BaseTool):
    """Tool that queries the Atlassian Jira API."""

    api_wrapper: AtlassianAPIWrapper = Field(default_factory=AtlassianAPIWrapper)  # type: ignore[arg-type]
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


class JqlJiraTool(JiraTool):
    """Tool to execute JQL query."""

    def _run(self, query: str) -> str:
        return self.api_wrapper.search(query)


class CreateIssueJiraTool(JiraTool):
    """Tool to create a new issue."""

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


class GetProjectsJiraTool(JiraTool):
    """Action to get Jira projects."""

    def _run(self) -> str:
        return self.api_wrapper.project()


class GetIssueTransitionsTool(JiraTool):
    """Action to get Jira issue transitions."""

    def _run(self, issue: IssueParam) -> str:
        query_dict = {"issue_key": issue.key}
        query = json.dumps(query_dict)
        return self.api_wrapper.get_issue_transitions(query)


class IssueTransitionTool(JiraTool):
    """Action to post Jira issue transition."""

    def _run(self, issue: IssueParam, transition: TransitionParam) -> str:
        query_dict = {"issue_key": issue.key, "status_name": transition.to}
        query = json.dumps(query_dict)
        return self.api_wrapper.issue_transition(query)


class CreatePageTool(JiraTool):
    """Tool to create a new page in Confluece."""

    def _run(self, title: str, body: str):
        query_dict = {
            "type": "page",
            "title": title,
            "space": "SD",
            "body":{
                "storage": {
                    "value": body,
                    "representation": "storage",
                }
            },
        }
        query = json.dumps(query_dict)
        return self.api_wrapper.page_create(query)
