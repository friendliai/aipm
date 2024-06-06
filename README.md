# AI PM

Meet AI PM, your expert AI Project Manager. It automates Jira issue creation from conversations and tracks sprint progress, revolutionizing your team's agile workflow and daily stand-up meetings.

In agile development, effective project management is crucial for success. We noticed that many teams struggle with organizing daily stand-ups and managing tasks efficiently. This inspired us to create AI PM, an intelligent project manager that seamlessly integrates with Jira to enhance productivity and streamline the agile process.

AI PM automates the creation of Jira issues based on team conversations, ensuring that no task is overlooked. It also tracks the progress of sprints by managing daily stand-up meetings, providing real-time updates and insights to keep the team on track and focused on their goals.

## Installation

```sh
poetry install
```

or

```sh
pip install -e .
```

## Prerequisites

You need to set the following environment variables:

- `JIRA_API_TOKEN`: Jira API token. Visit [Security page](https://id.atlassian.com/manage-profile/security) to manage your API token.
- `JIRA_USERNAME`: Jira email address.
- `JIRA_INSTANCE_URL`: Jira instance URL (e.g., "https://friendli.atlassian.net")
- `OPENAI_API_KEY`: OpenAI API key.

## Usage

### Sprint Planning

```sh
aipm planning
```

<a href="https://asciinema.org/a/662681" target="_blank"><img src="https://asciinema.org/a/662681.svg" /></a>

### Daily Standup

```sh
aipm standup
```

<a href="https://asciinema.org/a/662693" target="_blank"><img src="https://asciinema.org/a/662693.svg" /></a>
