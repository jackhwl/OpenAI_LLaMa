# Prompt 9: Build the Content Machine

> **Instructor note:** Two commands: /content-machine creates content, /content-plan plans the calendar. Show how the Notion database tags everything by platform, type, pillar, and idea. The vault stores the same content cross-linked. This is a content team, not a text generator.

Copy and paste the following into Claude Code:

```
/new

Context: This is build #9 of 10. Research outputs are in vault/research/. Brand info in vault/business/brand.md. soul.md has my voice. I need a content engine that produces deeply researched, platform-native content in my voice, properly tagged for planning and tracking.

Instruction: Build a Content Machine with TWO separate commands: /content-machine (create) and /content-plan (plan calendar).

COMMAND 1: /content-machine (Create Content)

Before running the pipeline, pull context from the vault first:
- Read vault/me/goals.md (what is the user trying to achieve? Content should serve those goals)
- Read vault/business/brand.md (company context, tone, what we never say)
- Read vault/business/ (products, services, positioning)
- Read vault/research/ (recent research that could inform this content)
- Read vault/people/ (who is the audience? who are the competitors?)
- Read vault/projects/content-machine/status.md (what content was already created? avoid repeating angles)
- Search Notion Content Library for past content on similar topics

With that context, the agent should already know the audience, the business angle, and the voice. Only ask follow-ups for what the vault DOESN'T answer:
- "Any specific hot take or angle you want to push on this?" (vault can't predict opinion)
- "Which platforms? All, or specific ones?" (unless user already said)
Keep it to 1-2 questions max. The vault should handle the rest. If the user gives a topic the vault has rich context on, skip straight to creation.

3-agent pipeline:
1. RESEARCHER: Read the source deeply. Extract key claims, data points, quotable lines, frameworks, counterintuitive insights. Search web for supporting stats and fresh angles. Don't just summarize. Find the insight that makes this worth sharing.
2. WRITER: Take the research brief + soul.md voice. Create platform-native content. Each piece follows the actual structure of that platform. Not just different word counts. Different formats, different hooks, different rhythms.
3. EDITOR: Load soul.md. Hard checks: no em-dashes, no filler, no parallel triplets, no uniform sentence length, no "it's worth noting." Score tone against soul.md examples. Rewrite anything that sounds like AI. The content must pass as human-written.

Content formats to generate:
- X thread (5-8 tweets. Hook tweet is everything. Punchy, opinionated. One insight per tweet. No hashtag walls.)
- LinkedIn post (150-300 words. Personal angle. Hook above the fold. Story structure. Hashtags at end.)
- Instagram caption (Hook line. Story body. CTA. Hashtag block after dot spacers.)
- TikTok/Reels script (Hook in 2 sec. 30-60 sec total. Text overlay notes for muted viewers. Camera/edit notes.)
- Newsletter draft (300-500 words. Personal opening. One deep take. P.S. kicker.)
- Blog/SEO (If source isn't already a blog. H1/H2 structure. 1500+ words. Internal links.)

Each piece gets full metadata tags:
- Platform (X/LinkedIn/Instagram/TikTok/Newsletter/Blog)
- Type (thread/post/caption/script/newsletter-section/long-form)
- Content Pillar (Brand/Product/Thought Leadership/Education/Community)
- Idea (one-line angle that makes this piece unique, the hook)
- Source (what it was derived from, link or reference)
- Target Audience (who this is for)

Save to vault AND Notion:
- Notion: Create "Content Library" database under Personal OS parent page. Columns: Title (title), Platform (select), Type (select), Pillar (select), Idea (text, the hook/angle), Source (text), Target Audience (text), Status (select: Idea/Draft/Review/Scheduled/Published), Publish Date (date). Write the FULL content in the Notion page body, organized with ## headers per platform.
- Vault: vault/projects/content-machine/kits/YYYY-MM-DD-{topic}.md with all content + metadata. Cross-link to vault/research/ if source was a research report, vault/business/ if about a product.
- Output files: outputs/content-machine/YYYY-MM-DD-{topic}/ with one .md file per platform format.

COMMAND 2: /content-plan (Plan Calendar)

When user runs /content-plan, pull vault context first:
- Read vault/me/goals.md (what's the user working toward? content should drive those goals)
- Read vault/business/ (products, launches, positioning)
- Read vault/research/ (research topics that could become content)
- Read vault/projects/content-machine/ (what's already been created and planned)
- Read Notion Content Library for existing calendar
- Read vault/business/competitors/ (what are competitors talking about? fill gaps or counter-position)

With that context, ask only what's needed:
1. "How many weeks?" (can't infer this)
2. If the vault shows an upcoming launch or milestone in goals.md: "I see {launch} coming up. Want me to plan content around it?" (don't ask, suggest)
3. If posting frequency isn't established yet: "How often per platform?"
2. Read existing Content Library in Notion for what's already planned/published
3. Read vault/research/ for research topics that could become content
4. Read vault/business/ for product and company topics
5. Read vault/me/goals.md for what the user is trying to achieve (content should serve goals)
6. Identify gaps: days without content, platforms underserved, pillars with no recent posts
7. Suggest topics. For each: title, platform, type, pillar, idea/angle, source material, suggested publish date
8. Present as a table. User approves, edits, or rejects each one.
9. Approved topics get added to the Notion Content Library with Status "Idea" and the suggested publish date
10. For each approved topic, tell the user: "Run /content-machine with '{topic}' to create the content."

The calendar in Notion shows: Calendar view (monthly), Pipeline board (by Status), By Platform (board), This Week (filtered table).

Input:
- Source (URL, text, topic, transcript, or vault/research/ report) for /content-machine
- soul.md for voice
- brand/config/brand-config.md for brand context
- Search Notion for related published content (avoid repeating same angle)
- Search web for supporting data

Output:
- work/09-content-machine/ with CLAUDE.md
- TWO commands: .claude/commands/content-machine.md and .claude/commands/content-plan.md
- Content kit at outputs/content-machine/YYYY-MM-DD-{topic}/ (one .md per platform)
- "Content Library" Notion database with full content in page body + all metadata tags
- Notion views: Calendar, Pipeline, By Platform, This Week
- vault/projects/content-machine/status.md with Notion database ID
- After creating content, update the vault with what was learned:
  - If the research uncovered new data or insights, add to vault/research/
  - If new competitors or people were mentioned, create vault/business/ or vault/people/ pages
  - If the user edited or rejected a piece, note what they didn't like in vault/me/writing-style-notes.md (the content machine gets better over time)
- Mark "Content Machine" as Done on sprint board
- On-demand only, no schedule
- Tell me: "Content Machine built. 9 of 10 done. Next: paste prompt #10 (Weekly Exec Report, the capstone)."
```

> **Instructor note:** Demo /content-machine with a research report. Open the Notion page, show all platform content with headers, all metadata tags filled. Then run /content-plan: "plan 2 weeks of content for my new course on Agentic AI Engineering Bootcamp." Show the calendar filling up. "Two commands: one creates, one plans. Everything tagged, everything in Notion, everything in your voice."
