# Prompt 10: Build the Weekly Exec Report (Capstone)

> Instructor note: This is the finale. It reads from EVERY other automation. The moment students see the whole system come together in one branded deck.

```
/new

Context: This is build #10 of 10, the capstone. All 9 other automations are running. You need a weekly report that aggregates data from every automation into one branded 7-slide PowerPoint deck.

Instruction: Build a Weekly Exec Report automation. Every Friday, read from ALL other automations: sprint tracker (project progress), morning brief highlights (vault/projects/morning-brief/history/), meeting notes (vault/meetings/), market pulse (vault/business/competitors/), CRM (vault/people/ for who you interacted with), expenses (vault/projects/expense-wrangler/), research (vault/research/), and content created (vault/projects/content-machine/ if it exists). Pull raw data from Gmail and Calendar. Ask the user: "PPT deck, PDF summary, or both?" Default to PPT. Generate a branded 7-slide deck using /pptx skill + brand template. Also create a Notion weekly summary page with the full report content in the page body.

Input:
- Notion MCP (read all databases: sprint board, CRM, expenses, meeting notes, market scans + create weekly summary page)
- Gmail MCP, Google Calendar MCP
- /pptx skill, brand/templates/template.pptx, brand/config/brand-config.md
- soul.md (reporting tone)
- vault/projects/sprint-tracker/, vault/projects/morning-brief/history/, vault/meetings/, vault/business/competitors/, vault/people/, vault/projects/expense-wrangler/, vault/research/, vault/projects/content-machine/

Output:
- work/10-weekly-exec-report/
- Command to run the automation
- Branded PPT at outputs/reports/weekly-exec-YYYY-MM-DD.pptx with 7 slides: week summary, project status, key meetings, market intel, relationships, blockers, next week priorities
- Notion weekly summary page under Personal OS parent
- vault/projects/weekly-exec-report/metrics-history/ for trend tracking
- Mark "Weekly Exec Report" as Done on sprint board
- Schedule: Friday at 4 PM
- Tell me: "Weekly Exec Report built. 10 of 10 done. All automations built. Your Personal OS is fully operational. Run /cron-setup to activate all schedules."
```

> Every slide pulled data from a different automation built today. This deck used to take 2-3 hours every Friday. It just happened in 90 seconds.
