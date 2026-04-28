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
  - Basic ComfyUI Workflow
    - Using lora model to speed up
    - Load LoRA
    - steps: 4
    - cfg: 1
    - sampler_name: lcm
    - scheduler sgm_uniform
  - Text to Image