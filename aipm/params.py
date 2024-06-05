"""Tool params."""

from __future__ import annotations

from langchain_core.pydantic_v1 import BaseModel, Field


class JqlParam(BaseModel):
    """JQL parameters."""

    query: str = Field(..., description="JQL query.")


class ProjectParam(BaseModel):
    """Schema for operations that require a Project name as input."""

    key: str = Field(..., description="The key of Jira project.")


class IssueTypeParam(BaseModel):
    """Schema for operations that require an IssueType as input."""

    name: str = Field(
        ..., description="The name of issue type. One of Epic, Story, Task, and Bug."
    )


class IssueTransitionParam(BaseModel):
    """Schema for operations that post issue transition"""

    issue_key: str = Field(..., description="The key of Jira issue.")
    status_name: str = Field(
        ..., description="Desired status. One of 'In Progress' and 'Done'"
    )


class CreateIssueParam(BaseModel):
    """Schema for operations that require task summary, project, and issuetype as input."""

    project: ProjectParam
    issuetype: IssueTypeParam
    summary: str = Field(..., description="The description of task.")
