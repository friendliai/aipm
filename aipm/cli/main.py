"""AI PM CLI."""

from __future__ import annotations

import typer
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

from aipm.agent import AgentMode, get_agent

app = typer.Typer(
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=True,
    pretty_exceptions_enable=False,
)


def _run_qa_pipeline(agent_executor: AgentExecutor) -> None:
    history = []
    while True:
        user_input = typer.prompt("🧑")
        answer = agent_executor.invoke({"input": user_input, "chat_history": history})
        typer.secho(f"🤖: {answer['output']}", fg=typer.colors.GREEN)
        history.append(HumanMessage(content=user_input))
        history.append(AIMessage(content=answer["output"]))


@app.command()
def planning(verbose: bool = typer.Option(False)):
    agent_executor = get_agent(AgentMode.PLANNING, verbose=verbose)
    _run_qa_pipeline(agent_executor)


@app.command()
def dailysprint(verbose: bool = typer.Option(False)):
    agent_executor = get_agent(AgentMode.DAILY_SPRINT, verbose=verbose)
    _run_qa_pipeline(agent_executor)
