# OpenAI Agents Python SDK : Agents as Tools

Example of a multi-agent system for code review in which an initial agent receives input and dynamically delegates tasks to specialized agents, treating them as callable tools.
[Documentation: OpenAI Agents SDK](https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/agents_as_tools.py)
---

[1]- Python installation
[2]- Create and activate a virtual Environment
[3]- Install packages
[4]- Create API keys & set the environment variables 

### [1]-Python installation

#### macOS
1. **Check if Python is already installed**
   ```sh
   python3 --version
   ```
   If Python is not installed, proceed with the steps below.

2. **Install Homebrew (if not installed)**
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Install Python**
   ```sh
   brew install python3
   ```

4. **Check Python Version**
   ```sh
   python3 --version
   ```

#### Windows
1. **Download Python** from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Run the installer** and check the box **"Add Python to PATH"** before proceeding with the installation.

3. **Check Python Version**
   ```sh
   python --version
   ```

---

### [2]-Create and activate a virtual environment - [venv](https://docs.python.org/3/library/venv.html)

#### macOS
1. **Navigate to your project directory**
   ```sh
   cd /path/to/your/project
   ```

2. **Create a virtual environment**
   ```sh
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**
   ```sh
   source .venv/bin/activate
   ```

4. **Verify that the virtual environment is active** (you should see `(venv)` in the terminal prompt).

#### Windows
1. **Navigate to your project directory**
   ```sh
   cd C:\path\to\your\project
   ```

2. **Create a virtual environment**
   ```sh
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   ```sh
   .venv\Scripts\activate
   ```

4. **Verify that the virtual environment is active** (Command Prompt should show `(venv)` before the directory path).

---

## Deactivating the Virtual Environment
For both macOS and Windows, deactivate the virtual environment by running:
```sh
 deactivate
```

---

### [3]-Install packages
(Mac)
```sh
pip3 install -r requirements.txt
pip3 install openai-agents
```

(Windows)
```sh
pip install -r requirements.txt
pip install openai-agents
```

---

## Exiting the Virtual Environment
```sh
deactivate
```

### [4]-Create API keys & set the environment variables 


#### 4.1 Setting Up OpenAI Secret Key  
1. Create an OpenAI Account[OpenAI's API Keys page](https://platform.openai.com/signup/),
2. Go to [OpenAI's API Keys page](https://platform.openai.com/settings/organization/api-keys),
3. Click **Create new secret key** and copy it, 
4. You will need to add your billing information (MANAGE > Settings > Billing).  

#### Set environment variables 

You can store the key in your shell configuration file:  

```sh
echo 'export OPENAI_API_KEY="your-secret-key"' >> ~/.bashrc
source ~/.bashrc
````

or add to `.env` file

```sh
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

### -Start the app
(Mac)
```sh
python3 main.py
```

(Windows)
```sh
python main.py
```

### Examples of Code Requests

* Add dark mode toggle with theme persistence
* Implement user authentication using JWT
* Create a search bar with live filtering
* Add pagination to API results
* Integrate file upload with drag-and-drop
* Build a responsive sidebar navigation
* Add toast notifications for user actions
* Implement form validation with error messages
* Add lazy loading for images and components
* Create a dashboard with dynamic charts
* Enable multi-language (i18n) support
* Implement infinite scrolling on the feed
* Add a favorites system with local storage
* Create a modal for user confirmation prompts
* Integrate Google Maps API for location input.


