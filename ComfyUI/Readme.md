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
  - 16. Canny ControlNet
  - 17. Depth ControlNet
  - 18. OpenPose ControlNet
    - DWPose
  - 19. IP-Adapter
  - 20. OpenPose ControlNet with Flux
  - 21. IP-Adapter with Flux
  - 22. ControlNets from Video
  - 23. AnimateDiff
  - 24. Video Helper Suite
  - 25. ControlNeXt SVD
  - 26. LTXV Text To Video
  - 27. LTXV Image To Video
  - 28. LTXV In Context LoRA Pose Control
  - 29. FLUX.1 Kontext
  - 30. FLUX.1 Kontext with Multiple Images
  - 31. Wan 2.2 Text to Video (T2V)
  - 32. Wan 2.2 Image to Video (I2V & FLF2V)
  - 33. Qwen Edit - Multiple Camera Angles
  - 34. Get Line Custom Node
  - 35. Lip Sync using Wan 2.2 (S2V)
  - 88. Aderant
  - 36. Wan 2.2 VACE Video Editing
  - 37. Wan 2.2 Animate - Character Replacement
  - 38. FLUX.2 Klein
    - Txt2Image Qwen-Image-2.1 MLS workflow
      - MLX 热启动基准 223.76 秒 vs 251.69 MPS, MLX 的耗时约少 11.1%
    - Qwen-Image-2.1-T2I-MPS.json
    - to start MLX @ http://127.0.0.1:8189/
    ```
   cd "$HOME/mlx-test-project/ComfyUI"

  "$HOME/mlx-test313/bin/python" main.py \
    --listen 127.0.0.1 \
    --port 8189 \
    --extra-model-paths-config "$HOME/mlx-test-project/models.yaml" \
    --input-directory "$HOME/ComfyUI-Shared/input" \
    --output-directory "$HOME/ComfyUI-Shared/output" 
    ```
    - Desktop version 8188: PyTorch MPS, including your working Qwen-Image 2.1 image-editing workflow.
    - 8189: MLXU, including your MLX text-to-image workflow.
  - on my Mac
  
| Feature | MPS | MLX |
|---|---|---|
| Full name | Metal Performance Shaders | MLX (framework name) |
| Developed by | Apple | Apple |
| Main purpose | GPU computation acceleration | Machine learning framework |
| Used with | PyTorch, other frameworks | MLX-native models and code |
| Apple Silicon GPU | Yes | Yes |
| Unified memory | Yes | Yes |
| Your ComfyUI | Desktop (8188) | MLXU (8189) |