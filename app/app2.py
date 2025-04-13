import streamlit as st
import faiss
import numpy as np
import pickle
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from groq import Groq

# --- CONFIG ---
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "12345678"
model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key="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")  # Replace this!

# --- Neo4j Driver ---
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# --- Streamlit Layout ---
st.set_page_config(page_title="Repo Doc Generator", layout="wide")
st.title("📄 GitHub Repo Documentation Generator")

# --- User Input ---
query_text = st.text_area("Enter your query ")

def query_neo4j(query_text):
    with driver.session() as session:
        results = session.run("""
            MATCH (n)
            WHERE (n:Function OR n:Variable OR n:File OR n:Configuration)
              AND toLower(n.name) CONTAINS toLower($query_text)
            RETURN labels(n)[0] AS type, n.name AS name
        """, {"query_text": query_text})
        return [(record["type"], record["name"]) for record in results]

# --- FAISS Search across all indexes ---
def query_faiss_combined(query_text, top_k=3):
    query_embedding = model.encode([query_text])
    results = []

    try:
        index_fn = faiss.read_index("faiss_functions.bin")
        with open("faiss_functions.pkl", "rb") as f:
            fn_texts = pickle.load(f)
        _, indices = index_fn.search(np.array(query_embedding), k=top_k)
        results += [f"🔧 Function: {fn_texts[i]}" for i in indices[0]]
    except Exception as e:
        results.append(f"❌ Function index error: {e}")

    try:
        index_var = faiss.read_index("faiss_variables.bin")
        with open("faiss_variables.pkl", "rb") as f:
            var_texts = pickle.load(f)
        _, indices = index_var.search(np.array(query_embedding), k=top_k)
        results += [f"📦 Variable: {var_texts[i]}" for i in indices[0]]
    except Exception as e:
        results.append(f"❌ Variable index error: {e}")

    try:
        index_file = faiss.read_index("faiss_files.bin")
        with open("faiss_files.pkl", "rb") as f:
            file_texts = pickle.load(f)
        _, indices = index_file.search(np.array(query_embedding), k=top_k)
        results += [f"📄 File: {file_texts[i]}" for i in indices[0]]
    except Exception as e:
        results.append(f"❌ File index error: {e}")

    return results

# --- LLM Prompt Function ---
def generate_response(graph_context, code_snippets, query):
    prompt = f"""Context from Code Graph:
{graph_context}

Relevant Code and Metadata:
{code_snippets}

{query}
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You're a code expert."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- Search & Explain ---
if st.button("🔍 Search & Generate Explanation"):
    graph_results = query_neo4j(query_text)
    faiss_results = query_faiss_combined(query_text)

    graph_context = "\n".join([f"🛠 {config} -> 📄 {file}" for config, file in graph_results])
    code_snippets = "\n".join(faiss_results)

    llm_response = generate_response(graph_context, code_snippets, query_text)

    st.subheader("LLM Explanation")
    st.markdown(f"**Graph Context:**\n{graph_context}")
    st.markdown(f"**Retrieved Snippets:**\n```text\n{code_snippets}\n```")
    st.markdown(f"**LLM Response:**\n{llm_response}")

# --- Full Documentation Generation ---
st.markdown("---")
st.subheader("📘 Generate Complete Project Documentation")
if st.button("📄 Generate Full Documentation"):
    try:
        all_texts = []

        with open("faiss_functions.pkl", "rb") as f:
            all_texts += pickle.load(f)
        with open("faiss_variables.pkl", "rb") as f:
            all_texts += pickle.load(f)
        with open("faiss_files.pkl", "rb") as f:
            all_texts += pickle.load(f)

        doc_prompt = f"""Generate detailed technical documentation for this codebase.
Describe the purpose of functions, key variables, and files based on the following metadata:

{chr(10).join(all_texts[:50])}  # Show sample of metadata
"""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a senior software documenter."},
                {"role": "user", "content": doc_prompt}
            ]
        )

        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"❌ Documentation generation failed: {e}")

# --- Close Neo4j Connection ---
driver.close()
