from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
import torch

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization_config=quantization_config,
    device_map="auto"
)


print(f"Model loaded on: {torch.cuda.get_device_name(0)}")
print(f"Memory allocated: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")


pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

messages = [
    {"role": "user", "content": "What equipment can remote employees request?"}
]

output = pipe(messages, max_new_tokens=150)

assistant_response = output[0]["generated_text"][-1]["content"]
print(assistant_response)