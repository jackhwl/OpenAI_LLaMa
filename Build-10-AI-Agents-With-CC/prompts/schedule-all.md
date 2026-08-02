# Activate All Schedules

> **Context:** Run this after you've built your automations. It reads your schedule registry and sets up system-level jobs for everything.

Copy and paste the following into Claude Code:

```
Run /cron-setup
```

> **What happens:** The agent reads scheduler/schedule.md, detects your OS, and creates system-level scheduled jobs for every registered task. Each job spins up a fresh Claude Code session at the scheduled time, runs the command, notifies you via Telegram, and exits. Your machine needs to be on for these to fire.
