"""WellnessGPT CLI welcome banner and session chrome."""
from __future__ import annotations

import sys
from typing import Any

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

from cli.theme import GREEN, MUTED, NAVY, NAVY_LIGHT, TEAL, TEAL_BRIGHT, VERSION, label_for_intent


def ensure_utf8_stdio() -> None:
    if sys.platform != "win32":
        return
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def _logo_art() -> Text:
    line1 = Text()
    line1.append("WELL", style=f"bold {NAVY}")
    line1.append("NESS", style=f"bold {TEAL}")
    line1.append("GPT", style=f"bold {GREEN}")
    return line1


def print_welcome_banner(console: Console, *, patient_name: str | None = None) -> None:
    subtitle = f"Session · {patient_name}" if patient_name else "Healthcare AI Assistant"
    stack = Group(
        Align.center(_logo_art()),
        Text(""),
        Align.center(Text("15-Agent LangGraph · Azure OpenAI · SQLite", style=f"bold {NAVY_LIGHT}")),
        Text(""),
        Align.center(Text(f"v{VERSION}", style=f"dim {MUTED}")),
        Align.center(Text(subtitle, style=f"italic {MUTED}")),
    )
    console.print()
    console.print(
        Panel(
            stack,
            border_style=TEAL,
            box=box.ROUNDED,
            padding=(1, 2),
            subtitle="[dim]Interactive CLI[/dim]",
            subtitle_align="center",
        )
    )
    console.print()


def print_session_hint(console: Console) -> None:
    console.print(
        Panel(
            "[dim]Type your health question below. The supervisor routes to one specialist agent.\n"
            "Commands: [bold red]exit[/bold red] · [bold red]quit[/bold red] · [bold red]/quit[/bold red][/dim]",
            border_style=NAVY_LIGHT,
            box=box.SIMPLE,
            padding=(0, 1),
        )
    )
    console.print()


def print_patient_panel(console: Console, patient: dict[str, Any]) -> None:
    conditions = patient.get("chronic_conditions") or []
    allergies = patient.get("allergies") or []
    if isinstance(conditions, str):
        conditions = [conditions]
    if isinstance(allergies, str):
        allergies = [allergies]

    body = (
        f"[bold]Name[/bold]       {patient.get('name', 'Unknown')}\n"
        f"[bold]Patient ID[/bold] {patient.get('id', '?')}\n"
        f"[bold]ABHA[/bold]       {patient.get('abha_id') or '[dim]not linked[/dim]'}\n"
        f"[bold]Conditions[/bold] {', '.join(conditions) if conditions else '[dim]none recorded[/dim]'}\n"
        f"[bold]Allergies[/bold]  {', '.join(allergies) if allergies else '[dim]none recorded[/dim]'}"
    )
    console.print(
        Panel(body, title="[bold green]Patient context[/bold green]", border_style="green", box=box.ROUNDED)
    )
    console.print()


def print_intent_routing(console: Console, intent: str, user_message: str) -> None:
    from rich.markup import escape

    agent_label = label_for_intent(intent)
    console.print(
        Panel(
            f"{escape(user_message[:500])}{'…' if len(user_message) > 500 else ''}",
            title="[bold cyan]Your question[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    )
    console.print(
        Panel(
            f"Routed to [bold]{escape(agent_label)}[/bold]  [dim](intent: {escape(intent)})[/dim]",
            title="[bold]Supervisor[/bold]",
            border_style=TEAL_BRIGHT,
            box=box.SIMPLE,
            padding=(0, 1),
        )
    )


def print_goodbye(console: Console) -> None:
    console.print()
    console.print(Panel("[dim]Session ended. Take care.[/dim]", border_style=MUTED, box=box.SIMPLE))
    console.print()
