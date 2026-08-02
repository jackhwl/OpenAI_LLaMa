# Prompt 11: Activate All Schedules

> **Instructor note:** Before pasting this prompt, students need an auth token. Walk them through: "Open a NEW terminal tab (Cmd+T). Run `claude setup-token`. It gives you a token starting with sk-ant-oat01-... Copy it. Come back here and paste it when the agent asks."

**Before pasting the prompt below, do this first:**

1. Open a **new terminal tab** (Cmd+T on Mac, Ctrl+Shift+T on Linux)
2. Run: `claude setup-token`
3. Copy the token it gives you (starts with `sk-ant-oat01-...`)
4. Come back to your Claude Code session
5. Paste the prompt below

Copy and paste the following into Claude Code:

```
Context: All 10 automations are built. Each one added its schedule to scheduler/schedule.md. I need to activate them all as cron jobs so they run automatically. I have my auth token ready from `claude setup-token`.

Instruction: Run /cron-setup. Ask me for my auth token (from claude setup-token). Then find binary paths, read schedule.md, create cron entries for each automation, run a self-test, and confirm. Each cron job runs `claude -p "Run /{command}" --dangerously-skip-permissions` with the auth token.

Input:
- My auth token (I'll paste it when you ask)
- scheduler/schedule.md for all scheduled tasks
- OS detection (crontab for Mac/Linux, Task Scheduler for Windows)

Output:
- Ask me for the auth token first
- A cron entry per scheduled automation, tagged with # personal-os:{name}
- Self-test (adds a test entry 2-3 min from now, verifies it fires, cleans up)
- Show: what was created, times, how to check logs
- Controls: /cron-setup off (pause all), /cron-setup off {name} (pause one), /cron-setup on (resume)
- Update vault/log.md
- Tell me: "All schedules activated. Your Personal OS runs on its own. /cron-setup off to pause anytime."
```

> **Instructor note:** "Open a new tab, run claude setup-token, copy the token, paste it here. That's the one-time auth. After that, cron runs everything unattended. To pause: /cron-setup off. To resume: /cron-setup on."
