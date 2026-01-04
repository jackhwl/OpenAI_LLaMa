# MLX version - Uses Mac GPU (Metal) natively
# Install: pip install mlx-lm

from mlx_lm import load, generate

# Load the model (automatically uses Metal GPU)
model, tokenizer = load("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit")

# Format the prompt using chat template
messages = [{"role": "user", "content": "What equipment can remote employees request?"}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# Generate response
response = generate(
    model,
    tokenizer,
    prompt=prompt,
    max_tokens=150,
    verbose=True  # Shows tokens/sec
)

print("\n--- Response ---")
print(response)

