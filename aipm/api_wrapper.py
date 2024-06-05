"""Jira API Wrapper"""

from __future__ import annotations

from langchain_community.utilities.jira import JiraAPIWrapper


class CustomJiraAPIWrapper(JiraAPIWrapper):
    def issue_transition(self, query: str) -> str:
        try:
            import json
        except ImportError:
            raise ImportError(
                "json is not installed. Please install it with `pip install json`."
            )

        params = json.loads(query)
        return self.jira.set_issue_status(**params)

    def run(self, mode: str, query: str) -> str:
        if mode == "jql":
            return self.search(query)
        elif mode == "get_projects":
            return self.project()
        elif mode == "create_issue":
            return self.issue_create(query)
        elif mode == "other":
            return self.other(query)
        elif mode == "create_page":
            return self.page_create(query)
        elif mode == "issue_transition":
            return self.issue_transition(query)
        else:
            raise ValueError(f"Got unexpected mode {mode}")
