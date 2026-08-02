# Prompt 7: Build Email Triage

> Instructor note: Draft replies must sound like the user. Uses CRM for sender context. If a student edits a draft, the system learns their style.

```
/new

Context: This is build #7 of 10. The CRM is running and provides sender context. You need email classification and reply drafting that sounds like the user, with two operating modes.

Instruction: Build an Email Triage automation with two modes. Interactive: show drafts one at a time, user approves/edits/skips, stage approved drafts as Gmail drafts using gmail_create_draft MCP tool. Scheduled: save all drafts to outputs/. Both modes classify emails as Act Now/Read Later/Archive, use the CRM Notion database for sender context, and add new senders to the CRM. If the user edits a draft, note the pattern in vault/me/writing-style-notes.md. Do NOT dump raw email content into vault, only intelligence (who, what, why).

Input:
- Gmail MCP
- Notion MCP (search CRM for sender context + create "Email Triage" database under Personal OS parent page)
- Gmail MCP gmail_create_draft (stage approved replies as drafts. Do NOT use Chrome for this.)
- soul.md (voice matching for drafts)
- vault/people/

Output:
- work/07-email-triage/
- Command to run the automation
- Notion "Email Triage" database with columns: Subject (title), Sender (text), Classification (select: Act Now/Read Later/Archive), Draft Status (select: Pending/Approved/Sent/Skipped), Date (date). Views: "Today" (filtered), "Pending Drafts" (filtered)
- vault/people/ updated for new senders (intel only, NOT email content)
- vault/me/writing-style-notes.md created if user edits drafts
- Mark "Email Triage" as Done on sprint board
- Schedule: 3x daily (9 AM, 1 PM, 5 PM)
"
```

> 50 emails triaged in 2 minutes. Each draft in their voice.
