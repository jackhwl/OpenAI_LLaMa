# Prompt 5: Build the Personal CRM

> Every contact from morning brief and market pulse is already in vault/people/. The CRM organizes them into a Notion database with relationship tracking.

```
/new

Context: This is build #5 of 10. vault/people/ already has contacts enriched by the Morning Brief. You need a CRM with a Notion database, follow-up tracking, and a Monday follow-up list that drafts emails in the user's voice.

Instruction: Build a Personal CRM automation. Create a Notion "Personal CRM" database. Populate it from vault/people/, Gmail contacts, and Calendar attendees. Track relationships and follow-up dates. Every Monday, generate a follow-up list. Draft follow-up emails in the user's voice and stage them as Gmail drafts using gmail_create_draft MCP tool.

Input:
- Google Calendar MCP, Gmail MCP
- Notion MCP (create CRM database under Personal OS parent page)
- Gmail MCP gmail_create_draft (stage follow-up emails as drafts. Do NOT use Chrome for Gmail.)
- soul.md (voice for emails)
- vault/people/, vault/meetings/

Output:
- work/05-personal-crm/
- Command to run the automation
- Notion "Personal CRM" database with columns: Name (title), Company (select), Role (text), Email (email), Last Contact (date), Follow-Up Date (date), Relationship Score (number 1-10), Status (select: Active/Warm/Cold/New), Tags (multi-select), Notes (text). Views: "All Contacts" (table), "Follow-Up This Week" (filtered), "By Company" (board)
- vault/projects/personal-crm/status.md with follow-up list and Notion database ID
- Mark "Personal CRM" as Done on sprint board
- Schedule: Monday at 8:30 AM
"
```

> Show the Notion CRM. Every person from their emails is now tracked.
