"""Hermes plugin for Ponytail."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

SKILL_COMMANDS = {
    "ponytail-review": "Review the current diff or provided target: bugs, security, load, missing tests, speed, and what to cut.",
    "ponytail-audit": "Audit the whole repo: bugs, security, load, missing tests, speed, and what to cut.",
    "ponytail-debt": "List every deliberate `shortcut:` comment and its upgrade path.",
    "ponytail-gain": "Show the measured-impact scoreboard (less code, less cost, more speed).",
    "ponytail-help": "Show the Ponytail command reference.",
}

ROOT = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "skills"


def _skill_prompt(command: str, args: str = "") -> str:
    tail = args.strip()
    target = f"\n\nUser arguments: {tail}" if tail else ""
    return (
        f"Load and follow the Hermes plugin skill `ponytail:{command}`. "
        f"{SKILL_COMMANDS[command]}{target}"
    )


def _slash_access_denied(event: Any, gateway: Any, command: str) -> bool:
    if gateway is None or event is None:
        return False
    checker = getattr(gateway, "_check_slash_access", None)
    source = getattr(event, "source", None)
    if checker is None or source is None:
        return False
    try:
        return checker(source, command) is not None
    except Exception:
        return True


def rewrite_gateway_command(event: Any = None, gateway: Any = None, **_: Any) -> dict[str, str] | None:
    """Rewrite authorized gateway /ponytail-* commands into normal agent prompts."""
    text = str(getattr(event, "text", "") or "").strip()
    if not text.startswith("/"):
        return None
    head, _, rest = text[1:].partition(" ")
    command = head.replace("_", "-").lower()
    if command not in SKILL_COMMANDS:
        return None
    if _slash_access_denied(event, gateway, command):
        return None
    return {"action": "rewrite", "text": _skill_prompt(command, rest)}


def _make_skill_command_handler(ctx: Any, command: str) -> Callable[[str], str]:
    def handler(raw_args: str) -> str:
        prompt = _skill_prompt(command, raw_args or "")
        injected = False
        try:
            injected = bool(ctx.inject_message(prompt))
        except Exception:
            injected = False
        if injected:
            return f"Queued `{command}` for the agent."
        return prompt

    return handler


def register(ctx: Any) -> None:
    """Register Ponytail skills and slash commands with Hermes."""
    for child in sorted(SKILLS_DIR.iterdir() if SKILLS_DIR.exists() else []):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)

    ctx.register_hook("pre_gateway_dispatch", rewrite_gateway_command)

    for command, description in SKILL_COMMANDS.items():
        ctx.register_command(
            command,
            _make_skill_command_handler(ctx, command),
            description=description,
            args_hint="[target or notes]",
        )
