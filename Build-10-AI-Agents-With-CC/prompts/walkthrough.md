# Walkthrough: Build From Scratch (personal-os/)

## Pre-Session
- Claude Code installed, Claude Max plan
- MCPs authenticated: Gmail, Calendar, Notion
- Obsidian installed
- Instructor has a fully built copy for demos

## Schedule

| Time | What | Duration |
|------|------|----------|
| 11:00 | Opening: show the finished system | 15 min |
| 11:15 | Setup: /setup (identity, brand, vault, Notion tracker) | 45 min |
| 12:00 | Build #1-4: Sprint Tracker, Morning Brief, Market Pulse, Research Team | 90 min |
| 1:30 | Lunch + catch up | 45 min |
| 2:15 | Build #5-7: Personal CRM, Meeting Intel, Email Triage | 60 min |
| 3:15 | Build #8-10: Expense Wrangler, Content Machine, Weekly Exec Report | 60 min |
| 4:15 | Prompt #11: Activate schedules + Dispatch demo | 20 min |
| 4:35 | Wrap-up | 10 min |

## Steps

### Opening
- Show your fully built system: personality, vault, Notion databases
- "This is what you're building today."

### /setup
Students open Claude Code in personal-os/. Run /setup.
1. Skills install + MCP verification (automatic)
2. Identity: paste LinkedIn/resume, writing samples, pick personality
3. Brand: drop assets or skip (uses defaults)
4. Wiki pages created with [[links]]
5. Notion parent page + progress tracker (10 To Do)
6. Open Obsidian

### Prompt #1: Sprint Tracker
- Paste from prompts/01-sprint-tracker/
- Creates: work folder, command, vault structure
- Show Notion board: 1 Done, 9 To Do

### Prompt #2: Morning Brief
- Paste from prompts/02-morning-brief/
- Pulls real Gmail and Calendar
- Show: brief output, Notion Daily Briefs database, new vault/people/ pages

### Prompt #3: Market Pulse
- Paste from prompts/03-market-pulse/
- Agent asks who to track. Students name competitors.
- Show: Chrome scraping competitor sites, branded report, Notion entry

### Prompt #4: Research Team
- Paste from prompts/04-research-team/
- Students give a research question
- Show: agent designs team, runs parallel agents, asks PPT or PDF, generates branded report

### Prompt #5: Personal CRM
- Paste from prompts/05-personal-crm/
- Show: Notion CRM database populated from vault/people/

### Prompt #6: Meeting Intel
- Paste from prompts/06-meeting-intel/
- Demo pre-meeting prep for an upcoming meeting
- Students paste or drop meeting notes. Show extraction.

### Prompt #7: Email Triage
- Paste from prompts/07-email-triage/
- Show: classification, draft replies in user voice, gmail_create_draft

### Prompt #8: Expense Wrangler
- Paste from prompts/08-expense-wrangler/
- Drop sample receipts from prompts/08-expense-wrangler/sample-data/
- Show: 4-sheet Excel with real formulas, Notion database

### Prompt #9: Content Machine
- Paste from prompts/09-content-machine/
- Give it a research report or URL
- Show: /content-machine creates 6 formats, /content-plan plans calendar

### Prompt #10: Weekly Exec Report (Capstone)
- Paste from prompts/10-weekly-exec-report/
- Show: reads from ALL 9 automations, generates branded PPT
- "Every slide pulled from a different automation you built today."

### Prompt #11: Activate Schedules
- First: "Open a new terminal tab. Run `claude setup-token`. Copy the token."
- Then paste from prompts/11-activate-schedules/
- Agent asks for the token, creates cron entries, runs self-test
- Show: /cron-setup on, /cron-setup off, /cron-setup off {name}

### Wrap-Up
- Show Dispatch from phone
- Show Obsidian graph (grown all day)
- Show Notion with all databases
- "10 automations, all connected, system runs on its own."
