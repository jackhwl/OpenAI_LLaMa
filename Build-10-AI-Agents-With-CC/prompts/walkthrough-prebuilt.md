# Walkthrough: Pre-Built Version (personal-os-prebuilt/)

All 10 automations are already built. You just set up your identity and start using them.

## Pre-Requisites
- Claude Code installed
- MCPs authenticated: Gmail, Calendar, Notion (run /mcp in any session)
- Obsidian installed

## Step 1: Run /setup (~15 min)

Open Claude Code in personal-os-prebuilt/. Run /setup.

What it asks:
- Paste LinkedIn/resume (or point to a file)
- Paste writing samples (posts, tweets, emails)
- Pick a personality ("Jarvis", "chill surfer", or describe a vibe)
- Drop brand assets or skip

What it creates:
- soul.md (your identity and voice)
- Vault pages (role, goals, business, people)
- Notion "Personal OS" parent page with Progress Tracker
- Obsidian vault ready to browse

## Step 2: Run each command

All commands are ready. Each creates its Notion database on first run.

| Command | What it does | Example input |
|---------|-------------|---------------|
| `/morning-brief` | Daily email + calendar + Notion summary | Just run it |
| `/market-pulse` | Scan competitors via Chrome + web search | "Track Jasper, Copy.ai, Buffer" (first run asks who) |
| `/research-team` | Multi-agent research on any topic | "Research AI agent frameworks for enterprise" |
| `/personal-crm` | Populate CRM from contacts, set follow-ups | Just run it (pulls from Gmail + Calendar) |
| `/meeting-intel` | Pre-meeting prep or post-meeting extraction | "Prep me for my 2pm" or drop a transcript in work/06-meeting-intel/inbox/ |
| `/email-triage` | Classify inbox, draft replies in your voice | Just run it |
| `/expense-wrangler` | Process receipts, generate branded Excel | "/expense-wrangler" then paste "$45 lunch at Kinka" or drop receipt PDF in work/08-expense-wrangler/inbox/ |
| `/content-machine` | Create content from any source | "Create content about AI agents for business" or paste a URL |
| `/content-plan` | Plan content calendar for N weeks | "Plan 2 weeks of content for LinkedIn and X" |
| `/weekly-exec-report` | Aggregates everything into branded PPT | Just run it (reads from all other automations) |

## Step 3: Activate schedules

Run `/cron-setup` to create local system jobs.

| Automation | Schedule |
|-----------|----------|
| Morning Brief | Daily 8 AM |
| Market Pulse | Daily 7 AM |
| Email Triage | 3x daily (9 AM, 1 PM, 5 PM) |
| Sprint Tracker | Weekdays 9 AM |
| Personal CRM | Monday 8:30 AM |
| Expense Wrangler | Monthly (last day) |
| Weekly Exec Report | Friday 4 PM |

Manage: `/cron-setup off` (pause all), `/cron-setup off morning-brief` (pause one), `/cron-setup on` (resume).

## Step 4: Add your own automations

Run `/new` and describe what you want. The agent creates the folder, command, Notion database, and vault structure.

## Tips
- Ask "status" anytime to see what happened
- Drop files into vault/sources/ and run /ingest to add knowledge
- Run /brand to update brand assets anytime
- Run /lint to check vault health
- The vault grows with every interaction. The system gets smarter over time.
