# Prompt 6: Build Meeting Intelligence

> Instructor note: Pre-meeting prep uses CRM data. Post-meeting: students drop a transcript, voice memo, or whiteboard photo. Action items go to sprint board. Contacts update CRM.

```
/new

Context: This is build #6 of 10. The CRM and sprint board are already running. You need pre-meeting dossiers and post-meeting processing that works with any file format dropped into an inbox folder.

Instruction: Build a Meeting Intel automation with two modes. Pre-meeting: pull CRM contacts for attendees, search Notion for relevant docs, web research on attendees, and generate a one-page prep dossier. Post-meeting: user drops a file into inbox/ (any format: .txt .md .pdf .vtt .mp3 .m4a .jpg .png) or pastes text. For audio files (.mp3, .m4a, .wav): check if openai-whisper is installed. If not, install it (pip install openai-whisper) and download the base model on first use. Transcribe the audio with whisper, then process the transcript. Tell the user: "Installed Whisper for voice transcription. Using the base model. If you need better accuracy for longer meetings, you can upgrade to small later." Extract decisions, action items, and follow-ups. Create Notion meeting notes. Add action items to the sprint board. Update CRM contacts. Draft a follow-up email in the user's voice.

Input:
- Google Calendar MCP, Gmail MCP
- Notion MCP (search + create "Meeting Notes" database under Personal OS parent page + update CRM + add to sprint board)
- Chrome (web research on attendees only)
- Gmail MCP gmail_create_draft (stage follow-up emails as drafts. Do NOT use Chrome for Gmail.)
- Python (parse transcripts), Read tool (PDFs, images)
- Whisper (auto-installed on first audio file: pip install openai-whisper, base model. Works on Mac/Windows/Linux.)
- soul.md (voice for follow-ups)
- vault/people/, vault/meetings/, vault/projects/

Output:
- work/06-meeting-intel/ with inbox/ folder
- Command to run the automation
- Notion "Meeting Notes" database with columns: Title (title), Date (date), Attendees (text), Action Items (number), Status (select: Prep/Complete/Follow-up Sent). Views: "Recent" (table sorted by date), "Pending Follow-ups" (filtered)
- vault/meetings/ updated with structured meeting notes
- vault/people/ updated for every attendee
- Sprint board tasks added from action items
- Mark "Meeting Intel" as Done on sprint board
- Not scheduled (on-demand: "prep me for my 2pm" or "process my meeting notes")
"
```

> Every meeting makes the system smarter. CRM enriched. Sprint board gets tasks. Weekly report gets data.
