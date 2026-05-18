"""WellnessGPT terminal interface."""
import cli._path  # noqa: F401 — bootstrap Backend/ on sys.path

from cli.main import main

__all__ = ["main"]
