---
name: ponytail-help
description: >
  Quick reference for ponytail skills and commands. One-shot display.
  Use for /ponytail-help, "ponytail help", "how do I use ponytail".
---

# Ponytail Help

Display this reference card when invoked. One-shot: display only, persist nothing.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **ponytail** | coding task, or `ponytail:ponytail` | The lazy-dev rules themselves: least new code, scoped to coding work. |
| **ponytail-review** | `/ponytail-review` | Quality review of a diff: bugs, security, load, missing tests, speed, what to cut. Each finding says what goes wrong and how to fix it. |
| **ponytail-audit** | `/ponytail-audit` | The same quality review for the whole repo, ranked. |
| **ponytail-debt** | `/ponytail-debt` | Harvest `shortcut:` comments into a tracked ledger. |
| **ponytail-gain** | `/ponytail-gain` | Measured-impact scoreboard: less code, less cost, more speed. |
| **ponytail-help** | `/ponytail-help` | This card. |

The `ponytail` skill loads on a coding task; say "stop ponytail" to drop it for
the rest of the session. Any skill is also invokable as `ponytail:<name>`.

## More

Full docs: the repository README.
