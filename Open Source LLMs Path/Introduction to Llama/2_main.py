from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import os

# Disable MPS completely to avoid compatibility issues with Llama 3.1
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"

# Note: MPS (Metal) has compatibility issues with Llama 3.1 attention mechanism
# Using CPU for reliable execution on Mac. For GPU acceleration on Mac,
# consider using llama.cpp or MLX which are optimized for Apple Silicon.
print("Using CPU (MPS has compatibility issues with Llama 3.1)")

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Load model - explicitly on CPU, using float16 to reduce memory usage
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,
    device_map={"": "cpu"},  # Force all layers to CPU
    low_cpu_mem_usage=True
)

print(f"Model dtype: {model.dtype}")


pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
    # device already set via device_map in model loading
)

messages = [
    {"role": "user", "content": "What equipment can remote employees request?"}
]

output = pipe(messages, max_new_tokens=150)

assistant_response = output[0]["generated_text"][-1]["content"]
print(assistant_response)