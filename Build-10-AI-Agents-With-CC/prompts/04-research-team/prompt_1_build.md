# Prompt 4: Build the Research Team

> Instructor note: The wow demo. Multiple agents running in parallel. Ask: PDF or PPT? Students see branded reports generated. Uses market pulse competitor data as context.

```
/new

Context: This is build #4 of 10. Market Pulse data lives in vault/business/competitors/. You need an adaptive multi-agent research system that designs its own team based on the question asked. Past research patterns are stored in patterns/ for reuse.

Instruction: Build an adaptive Research Team automation. For every question: analyze it, design the right agent team, check patterns/ for reusable architectures from past research, show the design for user approval, execute using sub-agents, and save the pattern for next time. After research is complete, ask the user: "Want this as a PPT deck or PDF?" Then generate the branded output using /pptx skill for decks (read brand/templates/template.pptx and brand/config/brand-config.md) or Python for PDF (using brand colors and fonts). Always generate a branded deliverable, not just a markdown file.

Input:
- Sub-agents (Agent tool), web search, Chrome (deep scraping), Python (data analysis, charts)
- Notion MCP (search for internal docs + create research page under Personal OS parent)
- /pptx skill (branded deck), /xlsx skill (data tables), brand templates
- soul.md (voice)
- vault/research/ (past work), vault/business/ (market data from market pulse)

Output:
- work/04-research-team/ with patterns/ subfolder
- Command to run the automation
- Ask user "PPT deck or PDF?" then generate using /pptx skill (for PPT) or Python/reportlab (for PDF) with brand colors and logo
- vault/research/{topic}.md with concise findings and key insights
- Reusable architecture patterns saved to patterns/
- Mark "Research Team" as Done on sprint board
- Not scheduled (on-demand: "research {topic}" or give it a question)
```

> Watch 4 agents running simultaneously. The branded deck is the moment people lose it.
