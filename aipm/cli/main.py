"""AI PM CLI."""

import typer
from langchain_core.messages import AIMessage, HumanMessage
from aipm.agent import agent_executor


app = typer.Typer(
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=True,
    pretty_exceptions_enable=False,
)

@app.command()
def planning():
    history = []
    while True:
        user_input = typer.prompt("🧑")
        answer = agent_executor.invoke({"input": user_input, "chat_history": history})
        typer.secho(f"🤖: {answer['output']}", fg=typer.colors.GREEN)
        history.append(HumanMessage(content=user_input))
        history.append(AIMessage(content=answer["output"]))

@app.command()
def dailysprint():
    ...
