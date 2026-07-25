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