# Prompt 3: Build Market Pulse

> **Instructor note:** Chrome opens competitor websites live. Students see real scraping happen. The branded report and Notion database make it tangible. After this, the morning brief has market context.

Copy and paste the following into Claude Code:

```
/new

Context: I'm building the Market Pulse automation for my Personal OS. Morning Brief is already running. I need daily competitive intelligence that feeds into my morning context and future research.

Instruction: Build a Market Pulse automation that scans competitors daily. Use Chrome to scrape their websites (pricing, product, careers pages). Web search for news and funding. Search Notion for internal docs. Tag findings as "Action Needed" or "FYI". Generate a branded report. If no watchlist exists, ask me who to track.

Input:
- Chrome automation for competitor website scraping
- Web search for news, funding, leadership changes
- Notion MCP: search for internal docs + create "Market Scans" database under Personal OS parent page
- soul.md for priority filtering
- brand/config/brand-config.md for report branding
- vault/business/competitors/ for existing competitor pages

Output:
- work/03-market-pulse/ folder with CLAUDE.md spec and watchlist.md
- .claude/commands/market-pulse.md
- Market brief at vault/projects/market-pulse/news-archive/YYYY-MM-DD.md
- "Market Scans" Notion database (Date, Companies Scanned, Action Items, FYI Count, Summary)
- Update vault/business/competitors/{company}.md with latest intel (summary only)
- Update vault/business/market/trends.md with sector trends
- Dense data (screenshots, full articles) in vault/projects/market-pulse/ tier 2
- Create vault/people/ for any named executives found
- Mark "Market Pulse" as Done on sprint board
- Add to scheduler/schedule.md: market-pulse, daily at 7:00 AM
- Update routing table, vault/index.md, vault/log.md
```

> **Instructor note:** "Job postings tell you a company's strategy. If they're hiring 10 ML engineers, they're building something." Show the competitor vault pages.
