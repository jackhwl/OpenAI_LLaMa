import torch
from transformers import AutoModel, AutoTokenizer
import os

# 1. Define the model name (from Hugging Face) or path to local files
model_name = "microsoft/DialoGPT-small"  # Example model - replace with your model
# Alternatively, for a local model:
# model_name = "./path/to/your/local/model"

# 2. Create output directory for inspection results
output_dir = "model_inspection"
os.makedirs(output_dir, exist_ok=True)

# 3. Load the model and tokenizer
print("Loading model and tokenizer...")
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 4. Basic model information
print(f"\nModel architecture: {type(model).__name__}")
print(f"Number of parameters: {sum(p.numel() for p in model.parameters()):,}")
print(f"Model device: {next(model.parameters()).device}")

# 5. Inspect model structure
print("\nModel structure:")
for name, module in model.named_children():
    print(f"- {name}: {type(module).__name__}")

# 6. Detailed weight inspection
print("\nInspecting weights by layer...")

# Open a file to save detailed analysis
with open(f"{output_dir}/weight_analysis.txt", "w") as f:
    f.write("Detailed Weight Analysis\n")
    f.write("=" * 50 + "\n\n")
    
    total_params = 0
    for name, param in model.named_parameters():
        if param.requires_grad:
            f.write(f"Layer: {name}\n")
            f.write(f"  Shape: {tuple(param.shape)}\n")
            f.write(f"  Size: {param.numel():,} parameters\n")
            f.write(f"  Mean: {param.mean().item():.6f}\n")
            f.write(f"  Std: {param.std().item():.6f}\n")
            f.write(f"  Min: {param.min().item():.6f}\n")
            f.write(f"  Max: {param.max().item():.6f}\n")
            f.write("-" * 30 + "\n")
            
            total_params += param.numel()
            
            # Print first few layers to console
            if len(name.split('.')) < 3:  
                print(f"{name}: {tuple(param.shape)} ({param.numel():,} parameters)")

    f.write(f"\nTotal trainable parameters: {total_params:,}\n")

# 7. Save a small sample of actual weight values
print("\nSaving weight samples...")
with open(f"{output_dir}/weight_samples.txt", "w") as f:
    f.write("Weight Value Samples\n")
    f.write("=" * 50 + "\n\n")
    
    for name, param in model.named_parameters():
        if param.requires_grad and param.numel() < 1000:  
            f.write(f"{name} (shape {tuple(param.shape)}):\n")
            f.write(f"Values: {param.data.flatten()[:10].tolist()}\n")  
            f.write("-" * 40 + "\n")

# 8. Save model configuration
print("Saving model configuration...")
model.config.to_json_file(f"{output_dir}/config.json")

# 9. Create a simple summary report
with open(f"{output_dir}/summary.txt", "w") as f:
    f.write("Model Inspection Summary\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Model: {model_name}\n")
    f.write(f"Architecture: {type(model).__name__}\n")
    f.write(f"Total parameters: {sum(p.numel() for p in model.parameters()):,}\n")
    f.write(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}\n")
    f.write(f"Model layers: {len(list(model.named_parameters()))}\n")

print(f"\nInspection complete! Results saved to '{output_dir}' directory")
print("\nFiles created:")
for file in os.listdir(output_dir):
    print(f"- {file}")