## Section 1: Introduction
  - Foreword
  - Install ComfyUI
    - upgrade ComfyUI
    ```
    cd ~/Jack/imageAI/ComfyUI
    git fetch --all --prune
    git pull
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt --upgrade
    cd ~/Jack/imageAI
    source .venv310/bin/activate      
    python3 ComfyUI/main.py
    ```