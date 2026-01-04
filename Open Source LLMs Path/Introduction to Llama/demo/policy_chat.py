import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import pipeline, BitsAndBytesConfig
import torch

# Page configuration
st.set_page_config(
    page_title="Globomantics Policy Assistant",
    layout="centered"
)

st.title("Globomantics Policy Assistant")
st.caption("Ask questions about company travel and equipment policies")

# Cache models so they load only once
@st.cache_resource
def load_models():
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    client = chromadb.PersistentClient(path="policy_db")
    collection = client.get_collection("globomantics_policies")
    
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True
    )
    
    llm = pipeline(
        "text-generation",
        model="meta-llama/Llama-3.1-8B-Instruct",
        model_kwargs={"quantization_config": quantization_config},
        device_map="auto"
    )
    
    return embedder, collection, llm

with st.spinner("Loading AI models..."):
    embedder, collection, llm = load_models()

def find_relevant_chunks(query, n_results=3):
    query_embedding = embedder.encode(query)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )
    return results['documents'][0]

def answer_question(question):
    chunks_found = find_relevant_chunks(question)
    context = "\n\n".join(chunks_found)
    
    messages = [
        {
            "role": "system",
            "content": """You are a helpful assistant answering questions about Globomantics company policies. 
Answer based on the provided context. Be direct and specific.
If the context contains relevant information, provide it clearly.
If the context has no relevant information, say so."""
        },
        {
            "role": "user", 
            "content": f"Policy context:\n{context}\n\nQuestion: {question}"
        }
    ]
    
    response = llm(
        messages, 
        max_new_tokens=300, 
        temperature=0.1,
        pad_token_id=llm.tokenizer.eos_token_id
    )
    return response[0]["generated_text"][-1]["content"]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new input
if prompt := st.chat_input("Ask about company policies..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and show response
    with st.chat_message("assistant"):
        with st.spinner("Searching policies..."):
            answer = answer_question(prompt)
            st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar with examples
with st.sidebar:
    st.header("Example Questions")
    st.markdown("""
    - What's the hotel limit for SF?
    - Do I need receipts for meals?
    - What equipment do hybrid employees get?
    """)
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()