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

        python -m ipykernel install --user --name=venvI'
    ```
## Module 2: Reflection Design Pattern
  - Reflection to improve outputs of a task