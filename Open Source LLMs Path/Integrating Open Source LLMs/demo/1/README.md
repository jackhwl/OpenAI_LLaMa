# Ensuring Reliability & Security in LLM Integration

> This project showcases how to integrate, test and compare LLM providers : **Anthropic, Mistral**, and **OpenAI**, 
> **Key points:** API usage & rate limits (handling quotas, limits, and usage tracking), and error handling.
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
```

(Windows)
```sh
pip install -r requirements.txt
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

#### 4.2 Setting Up Anthropic Secret Key  
1. Create an Anthropic account : https://console.anthropic.com/,
2. In the Console ([MANAGE > Settings](https://console.anthropic.com/settings/keys)), select API Keys and click 'Create key',
3. Copy the generated key immediately and store it securely (you usually can't view it again).
4. You will need to add your billing information ([MANAGE > Settings > Billing](https://console.anthropic.com/settings/billing)).

#### 4.3 Setting Up Mistral Secret Key  
1. Create a [Mistral account](https://console.mistral.ai/),
2. Create or select a Workspace, go to API keys in the [workspace/organization settings](https://console.mistral.ai/api-keys), and click 'Createnew key',
3. Copy the new key and store it securely (you’ll need it for requests and integrations).


#### Set environment variables 

You can store the key in your shell configuration file:  

```sh
echo 'export OPENAI_API_KEY="your-secret-key"' >> ~/.bashrc
source ~/.bashrc
````

or add to `.env` file

```sh
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY"
MISTRAL_API_KEY="YOUR_MISTRAL_API_KEY"

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

