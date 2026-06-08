"""Rich-based terminal output for the CLI."""
from __future__ import annotations

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.rule import Rule

from cli.theme import label_for_intent, style_for_intent


def print_error(console: Console, message: str) -> None:
    console.print(f"[error]Error:[/error] {escape(message)}")


def print_answer_start(console: Console, intent: str) -> None:
    label = label_for_intent(intent)
    style = style_for_intent(intent)
    console.print()
    console.print(Rule(f"[{style}]{label}[/{style}]", style="dim"))


def print_answer_token(console: Console, token: str) -> None:
    if token:
        console.print(token, end="", highlight=False)


def print_answer_end(console: Console) -> None:
    console.print()
    console.print(Rule(style="dim"))
    console.print()
