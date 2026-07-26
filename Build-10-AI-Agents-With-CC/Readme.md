## Section 1: Introduction to Masterclass, Claude Superpowers Showcase, & Key Success Tips
  - 1. Masterclass Introduction & Your Personal Agent in Claude Superpowers Showcase
  - 2. Masterclass Outline and Learning Objectives
  - 3. Masterclass Key Success Tips
  - 4. Download the Masterclass Materials
  - 5. Claude Desktop App Setup
## Section 2: Claude Cowork Foundations Masterclass
  - 6. Claude Cowork Practical Demo: Develop PowerPoint Slides without a Skill
  - 7. Understanding Agent Skills & Popular Skill Sources
    - https://skills.sh
    - https://github.com/anthropics/skills/tree/main/skills
    - https://www.skillhub.club/
    - https://github.com/claude-office-skills
  - 8. Download a New Agent Skill and Upload it to Cowork
  - 9. Claude Cowork Practical Demo: Develop PowerPoint Slides with a Skill
'''
    Context: I have a CSV file with quarterly sales data for NovaTech Solutions, a SaaS company. The data covers all of 2025 across 3 regions (North America, Europe, Asia Pacific) and 2 product lines (Cloud Services, Consulting). Each row has the month, quarter, region, product line, revenue, units sold, and target. I need to present this to the C-suite at our annual review.

    Instruction: Create a executive presentation from this data. This deck will be presented by the VP of Sales to the C-suite. Use the ppt-visual-SKILL.md to design the presentation. Use all available PPT skills you have to make this the best possible presentation. Make it next level. 

    Input:
    - Data source: quarterly_sales.csv (uploaded to this conversation)
    - Company: NovaTech Solutions
    - Audience: C-suite executives
    - Tone: Confident, data-driven, forward-looking

    Output:
    - A file called novatech_annual_review_v2.pptx
'''
  - 10. Understanding Claude Plugins (Finance, Data, HR)
    - plugins bundle skills, connectors, slash commands & sub-agents into one package for a specific job function. No technical knowledge required to create them.
  - 11. Claude Plugin Demo: Build Dashboard & Explore Data Using Data Plugin in 
  - 12. How to Track Claude Token Usage & Limits
## Section 3: Claude Code Foundations Masterclass
  - 15. Claude Code Setup Using Desktop App (Optional, skip of already configured)
  - 16. Claude Code Setup in VS Code (Optional, skip if already configured)
  - 17. Claude Code Demo: Build with Claude Code in the Desktop App
    '''

Context: I run an AI-powered fitness coaching brand called "Elevate Performance." I want a website page I can open in my browser that helps users assess their fitness level and receive a personalized training plan.

Instruction: Create a single file called "elevate.html" with everything a client would need — a clean modern fitness dashboard, an interactive fitness assessment flow (step-by-step, not a long form), progress visualizations, personalized workout recommendations, and a membership signup section.

Implement it without using any frameworks or external libraries.

Input:

- Business name: Elevate Performance
- Tagline: "Train smarter. Perform better."
- Intake questions:
	Fitness goal? (Lose weight, Build muscle, Improve endurance, General fitness)
	How many days per week can you train? (input number)
	Current fitness level? (Beginner, Intermediate, Advanced)
	Biggest challenge? (Consistency, Nutrition, Motivation, Time)
- Logic:
	Generate a fitness readiness score
	Show level (Starter / Active / High Performance)
	Give 2–3 personalized recommendations based on answers
- Dashboard:
	Show weekly training capacity visually (simple bar or progress style)
	Show readiness score %
- Membership section:
	Name, email, preferred training time, notes

Output: A single HTML file I can open in any browser — it should feel like a real premium fitness-tech platform, the intake should be smooth (one question at a time), recommendations should update dynamically, and the UI should look polished enough to impress potential clients. Use the frontend-design skill and install it if you don't have it.

    '''
  - 18. Slash Commands in Claude Code
  - 19. Claude Code Demo: Build Dashboard Using Claude Code in VS Code (No Skills)
     '''
Context: I want to build a stock portfolio dashboard as a single HTML file I can open in my browser.

Instruction: First, check if a file called stock_data.csv exists in the current folder. If it does not exist, run a Python script to download the latest stock prices using yfinance and save them to stock_data.csv. Then build a dashboard.html file from that data using plain HTML, CSS, and JavaScript. Do not use any design skill. Style it with basic CSS only — functional layout, default colors, nothing fancy.

Input:
- Stocks: AAPL, MSFT, GOOGL, AMZN, NVDA, JPM
- CSV columns: symbol, name, price, change, change_pct
- Install yfinance if needed: pip install yfinance

Output:
- stock_data.csv with real current prices
- dashboard.html showing:
  - Header with total portfolio value and overall daily change
  - A card for each stock with name, price, and daily change
  - Green tint for stocks that are up, red tint for stocks that are down
  - A bar chart comparing daily % change across all 6 stocks
  - Basic responsive layout

     '''
  - 20. Install the front-end Design Skill in Claude Code in VS Code
    - npx skills add anthropics/claude-code --skill frontend-design
  - 21. Claude Code Demo: Build Dashboard Using Claude Code in VS Code (with Skills)
  '''
Context: I have stock_data.csv with real prices for 6 stocks and a basic dashboard.html that shows the data.

Instruction: Use the /frontend-design skill to build a new file called dashboard_v2.html. Make the most visually impressive financial dashboard you can — professional, polished, something you would actually show to a client. Keep all the same data and functionality from dashboard.html but make the design dramatically better.

Input:
- Same stock_data.csv from the current folder
- Same 6 stocks, same prices and daily changes
- Same bar chart comparing daily % change
- No constraints on design — go all out

Output:
- dashboard_v2.html in the same folder
- Professional financial dashboard with a clear design direction
- All data and functionality preserved
- The visual difference from dashboard.html should be dramatic
  '''
  - 22. Practice Opportunity Question: Claude Code with Skills in VS Code
  - 23. Practice Opportunity Solution: Claude Code with Skills in VS Code
```
Context: Building a single HTML file landing page for a pet grooming business. No frameworks, no dependencies. Don't use frontend design skill. 

Instruction: Create a single HTML file called "mindful_paws.html" for a boutique pet grooming salon called "Mindful Paws". Include a hero section with the tagline "Where grooming meets calm", an interactive booking quiz that asks 3 questions one at a time (pet type, size, service) and shows a price estimate, a services section with 4 services and prices, a gallery section with image placeholders, and a booking form with pet name, owner name, phone, and preferred date. Make it fully functional with smooth transitions.

Input:
- Business: Mindful Paws
- Tagline: "Where grooming meets calm"
- Services: Bath & Brush ($45), Full Groom ($75), Spa Day ($120), Puppy First Groom ($55)

Output: A single self-contained HTML file I can open in any browser. File name: mindful_paws.html
```

```
Context: Building a single HTML file landing page for a pet grooming business. No frameworks, no dependencies. Use frontend design skill. 

Instruction: Create a single HTML file called "mindful_paws.html" for a boutique pet grooming salon called "Mindful Paws". Include a hero section with the tagline "Where grooming meets calm", an interactive booking quiz that asks 3 questions one at a time (pet type, size, service) and shows a price estimate, a services section with 4 services and prices, a gallery section with image placeholders, and a booking form with pet name, owner name, phone, and preferred date. Make it fully functional with smooth transitions.

Input:
- Business: Mindful Paws
- Tagline: "Where grooming meets calm"
- Services: Bath & Brush ($45), Full Groom ($75), Spa Day ($120), Puppy First Groom ($55)

Output: A single self-contained HTML file I can open in any browser. File name: mindful_paws.html
```
  - 24. Context Window Management
  - 25. CLAUDE.md Best Practices & How to Create one with Claude Code
    - /init to create CLAUDE.md
  - 26. Model Context Protocol (MCP)
  - 27. Develop Slash Command Automation Demo (Part 1) - Research Teams
```
Context: I hold Apple (AAPL) as a core position in my portfolio. I just did deep research on the company using their 10-K and earnings call. Now I need a real-time update on how Apple is performing today, what the current sentiment is, and whether there is any breaking news I should know about.

Instruction: Search online for the latest Apple performance data, analyst sentiment, social media sentiment, and news. Give me a comprehensive update I can review in under 2 minutes.

Input:
- Stock to monitor: Apple (AAPL)
- Data points to find:
  - Current price and daily change ($ and %)
  - Key metrics: market cap, P/E ratio, 52-week range, volume vs average
  - Analyst sentiment: recent upgrades/downgrades, average price target, buy/hold/sell consensus
  - Social/retail sentiment: what are people saying on financial forums, X (Twitter), Reddit about Apple today
  - Recent news (last 24-48 hours): iPhone demand, AI announcements, App Store/regulatory updates, earnings commentary, supply chain developments, competitor moves (Microsoft, Google, Samsung)
  - Overall sentiment rating: bullish, bearish, or neutral with a brief explanation
- Also include: S&P 500 (SPY) and Nasdaq (QQQ) as benchmarks

Output:
- A clean, structured Apple monitor report with:
  - Market context at the top (SPY, QQQ, macro news affecting tech)
  - Apple price and performance section
  - Analyst sentiment section with specific names/firms if available
  - Social/retail sentiment section summarizing the mood
  - News section with key headlines
  - Overall assessment: bullish/bearish/neutral with reasoning

```
  - 28. Develop Slash Command Automation Demo (Part 2) - Develop Reports in Excel
```
Context: You just gathered comprehensive Apple performance data including price, analyst sentiment, social sentiment, and news. I need this organized into a clean Excel tracker that I can reference throughout the day and build historical records over time.

Instruction: Take the Apple update you just compiled and organize it into a professional Excel report with structured data and visual indicators.

Input:
- Source: The Apple analysis from our previous prompt in this conversation
- Stock: Apple (AAPL)
- Benchmarks: SPY, QQQ
- Today's date and time

Output:
- A file called apple_monitor.xlsx with:
  - A "Dashboard" sheet containing: date/time, Apple price, daily change, overall sentiment rating, and benchmark comparison (AAPL vs SPY vs QQQ daily change in a bar chart)
  - A "Fundamentals" sheet with: market cap, P/E ratio, 52-week range, volume, and key metrics
  - A "Sentiment" sheet with: analyst consensus, recent ratings, social sentiment summary, and overall mood
  - A "News" sheet with: headlines, source, date, and impact rating (positive/negative/neutral)
  - Color coding: green for positive, red for negative, yellow for neutral
  - Clean formatting with headers and number formatting
```
  - 29. Develop Slash Command Automation Demo (Part 3) - Create Slide Deck in PowerPoint
```
Context: We have a complete Apple monitoring report with price data, analyst sentiment, social sentiment, and news organized in Excel. I want to turn this into a short deck I can quickly review or share with my investment group.

Instruction: Create a PowerPoint deck from the Apple monitoring data. Keep it concise and visual. Each slide should communicate one key insight.

Input:
- Source: The Apple analysis and Excel data from our previous prompts
- Stock: Apple (AAPL), benchmarks SPY and QQQ
- Today's date and time

Output:
- A file called apple_update.pptx with:
  - Slide 1: Title slide with "Apple (AAPL) Monitor" and today's date/time
  - Slide 2: Price snapshot with current price, daily change, and comparison to SPY/QQQ
  - Slide 3: Analyst sentiment summary with consensus, recent ratings, and price targets
  - Slide 4: Social and retail sentiment with key themes from forums and social media
  - Slide 5: Key news headlines with impact assessment
  - Slide 6: Overall assessment: bullish/bearish/neutral, what to watch, and next catalyst
  - Clean, professional design
```
  - 30. Develop Slash Command Automation Demo (Part 4) - Develop an Automated Workflow
```
Context: We just built a 3-step workflow in this conversation: (1) search for Apple performance, sentiment, and news, (2) organize it into an Excel tracker, and (3) create a PowerPoint update deck. I want to turn this into a single reusable command so I can monitor Apple with one word.

Instruction: Create a Cowork command called /apple-monitor that chains all three steps together automatically. When I run /apple-monitor, it should do the full workflow end to end.

Input:
- Step 1: Search online for latest AAPL performance (price, change, metrics, analyst sentiment, social sentiment, news) plus SPY and QQQ benchmarks
- Step 2: Organize into apple_monitor.xlsx (dashboard with chart, fundamentals, sentiment, news sheets)
- Step 3: Create apple_update.pptx (6 slides: title, price snapshot, analyst sentiment, social sentiment, news, overall assessment)

Output:
- A working Cowork command called /apple-monitor
- When I type /apple-monitor in a new conversation, all three steps run automatically
- Confirm the command is created and ready to use
```
  - 31. Develop Slash Command Automation Demo (Part 5) - Schedule an Automation
```
Context: I created an /apple-monitor command that searches for Apple performance, sentiment, and news, creates an Excel tracker, and generates an update deck. I want this to run automatically every 2 hours during market hours so I always have a fresh Apple snapshot with the latest sentiment.

Instruction: Schedule /apple-monitor to run every 2 hours on weekdays during US market hours. I should have fresh Apple updates throughout the trading day without doing anything manually.

Input:
- Command to schedule: /apple-monitor
- Schedule: Every 2 hours on weekdays
- Market hours: 9:30 AM to 4:00 PM Eastern Time (approximately 9 AM, 11 AM, 1 PM, 3 PM)
- No runs on weekends

Output:
- The /apple-monitor command scheduled and confirmed
- Show me where to find the schedule settings so I can edit, pause, or cancel it later
```
## Section 4: Your Personal AI Agent Architecture in Claude Code & Cowork
  - 32. The Rise of Autonomous Personal AI Agents (OpenClaw, Hermes, & Claude Code)
    - Personality soul.md
    - Memory Karpathy Wiki Pattern
    - Automation
  - 33. Building Personal AI Agent Architecture (Deep Dive)
  - 34. The Karpathy Wiki Pattern
  - 35. Obsidian
    - obsidian is the viewer, claude code is the programmer, the wiki is the knowledge base contained in markdown files.
    - open vault/folder as an obsidian vault
    - claude code edits pages, you browse in real-time
    - graph view reveals orphan pages and clusters
  - 36. Personal AI Agent Folder Structure
    - personal-os/
      - CLAUDE.md
      - soul.md
      - GETTING-STARTED.md
      - SCHECULING-GUIDE.md
      -.claude/
        - settings.json
        - commands/ (7 commands)
      - brand/
        - config/ | images/ | templates/
      - vault/
        - me/ | business/ | people/
        index.md | log.md