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
    using ComfyUI Desktop doesn't need python3 ComfyUI/main.py
    ```
  - 3. Basic ComfyUI Workflow
    - Using lora model to speed up
    - Load LoRA
    - steps: 4
    - cfg: 1
    - sampler_name: lcm
    - scheduler sgm_uniform
  - 4. Text to Image
  - 5. Image to Image
    - https://sbcode.net/genai/img-2-img/
  - 6. Inpainting
    - 512-inpainting-ema.safetensors
  - 7. Outpainting
  - 8. The ImageCompositeMasked Node
  - 9. Subgraphs
  - 10. Install ComfyUI Manager
  - 11. ESRGAN
  - 12. Model Checkpoint Comparison
    - SD 1.5, SD 2.1, SDXL, Flux Dev, Flux Schnell, DreamShaper 8, AbsoluteReality, DreamShaper XL Turbo and RealismEngineSDXL.
  - 13. Latent Upscaling
  - 14. Stable Video Diffusion
    - https://sbcode.net/genai/svd/
    - fish 900 seconds
  - 15. Frame Interpolation