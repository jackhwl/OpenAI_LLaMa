# Prompt 2: Build the Morning Brief

Copy and paste the following into Claude Code:

```
/new

Context: I'm building the Morning Brief automation for my Personal OS. This is build #2 of 10. Sprint Tracker is already running. I need a daily summary of my emails, calendar, and relevant Notion context, filtered through my priorities from soul.md.

Instruction: Build a Morning Brief automation that pulls my unread emails, today's calendar, and searches Notion for project context. Filter through my priorities in soul.md. Create a branded summary and a Notion "Daily Briefs" database.

Input:
- Gmail MCP: unread emails from last 12 hours
- Google Calendar MCP: all events today
- Notion MCP: search for relevant project pages and context
- soul.md for priority filtering and voice
- vault/me/goals.md for current goals
- vault/people/ for context on calendar attendees
- brand/config/brand-config.md for branded output

Output:
- work/02-morning-brief/ folder with CLAUDE.md spec
- .claude/commands/morning-brief.md
- Morning brief saved to vault/projects/morning-brief/history/YYYY-MM-DD.md
- "Daily Briefs" Notion database under Personal OS parent page (Date, Summary, Urgent Count, FYI Count)
- Brief sections: Urgent, Today's Calendar, Key Context, FYI
- Scannable in under 3 minutes
- Create vault/people/{name}.md for every new person found in emails or calendar
- Create vault/business/{company}.md for new companies
- Mark "Morning Brief" as Done on sprint board
- Add to scheduler/schedule.md: morning-brief, daily at 8:00 AM
- Update routing table, vault/index.md, vault/log.md
"
```

> **Instructor note:** Show the Notion Daily Briefs database appearing. Show Obsidian graph growing with new people pages. "Tomorrow morning at 8 AM, this runs automatically."
