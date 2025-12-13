## Module 1: Introduction to Agentic Workflows
  - Welcome
  - What is agentic AI
  - Degrees of autonomy
  - Benefits of agentic AI
  - Agentic AI applications
  - Task decomposition: Identifying steps in a workflow
    - one step
    - 3-step workflow
    - 5-step workflow
    - building block
      - Models: LLMs
      - Tools: API, Information retrieval, Code execution
  - Evaluation agentic AI (evals)
  - Agentic Design Patterns
    - Reflection
    - Tool use
      - Analysis
        - Code Execution
        - Wolfram Alpha
        - Bearly Code Interpreter
      - Information gathering
        - Web search
        - Wikipedia
        - Database access
      - Productivity
        - Email
        - Calendar
        - Messaging
      - Images
        - Image generation
        - Image captioning
        - OCR
    - Planning
    - Multi-agentic workflows
    - Optional: Set up your local environment for the ungraded labs

    ```
        Make sure you have Python 3.10+ installed.

        (Recommended) Create and activate a virtual environment:

            python -m venv venv
            source venv/bin/activate     # On Windows: venv\Scripts\activate
        Create a new file named requirements.txt and copy the code provided at the end of this section.

        Install all required libraries:

            pip install -r requirements.txt
        (Optional) Link this environment to your IDE or Jupyter notebook:

        python -m ipykernel install --user --name=venv'
    ```
## Module 2: Reflection Design Pattern
  - Reflection to improve outputs of a task
  - Why not just direct generation?
  - Chart generation workflow
  - Ungraded Lab: Chart Generation
  - Evaluating the impact of reflection
    - Objective evals
      - Code-based evals are easier
      - Build a dataset of ground truth examples
    - Subjective evals
      - Use LLM as a judge
      - Rubric-based grading is better
  - Using external feedback
    - Mentioning competitiors
    - Fact checking an essay
    - LLM won't follow output length guidelines
  - Ungraded Lab: Improving SQL Generation with Reflection
## Module 3: Tool use
  - What are tools?
  - Creating a tool
  - Tool syntax
  - Ungraded Lab: Turning functions into tools
  - Ungraded Lab: Email Assistant Workflow
  - Code execution
  - MCP
## Module 4: Practical Tips for Building Agentic AI
  - Evaluations (evals)
    - Quick and dirty is ok to start!
    - As you find places where your evals fail to capture human judgement as to what system is better, use that as an opportunity to improve the metric
    - Look for places where performance is worse than humans
  - Errors analysis and prioritizing next steps
    - Develop a habit of looking at traces
    - Carry out error analysis to figure out what component performed poorly, leading to a poor final output
    - Use error analysis output to decide where to focus efforts
  - More error analysis examples
  - Component-level evaluations
  - Ungraded Lab: Adding a component-level eval to the research workflow 
  - How to address problems you identify
    - Developing intuition for model intelligence
      - play with models often
        - Having apersonal set of evals might be helpful
        - Read other people's prompts for ideas of how to best use models
