# Prompt 1: Build the Sprint Tracker

> **Instructor note:** This is the first automation students build. The Notion project board was already created during /setup with 10 tasks set to To Do. This prompt adds standup and velocity tracking. Every automation built after this marks itself Done on the board.

Copy and paste the following into Claude Code:

```
/new

Context: I'm building my first automation inside my Personal OS. My Notion progress tracker was created during /setup with 10 automations to build. The database ID is in vault/projects/sprint-tracker/status.md. I need a sprint tracker that reads this board and generates standup summaries.

Instruction: Build a Sprint Tracker automation. Read the Notion progress board, generate a standup summary (Done, In Progress, To Do with counts), and track velocity over time. Also ensure that every future automation marks itself Done on this board when built.

Input:
- Notion sprint board database ID from vault/projects/sprint-tracker/status.md
- vault/projects/ for any existing project context
- soul.md for voice and priority filtering

Output:
- work/01-sprint-tracker/ folder with CLAUDE.md spec
- .claude/commands/sprint-tracker.md
- Standup summary at vault/projects/sprint-tracker/standups/YYYY-MM-DD.md
- A Notion page for the standup under the Personal OS parent page
- Mark "Sprint Tracker" as Done on the Notion board
- Add to scheduler/schedule.md: sprint-tracker, weekdays at 9:00 AM
- Update routing table in CLAUDE.md
- Update vault/index.md and vault/log.md
```

> **Instructor note:** After this runs, show the Notion board: 1 Done, 9 To Do. This tracker is the spine of the workshop. Every subsequent prompt updates it.

