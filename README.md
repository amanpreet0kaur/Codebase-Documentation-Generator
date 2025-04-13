Here’s a clean and professional `README.md` for your **GitHub Repo Documentation Generator** project:

---

# 📄 GitHub Repo Documentation Generator

A powerful Streamlit-based tool that combines **Neo4j**, **FAISS**, **Sentence Transformers**, and **Groq LLM** to generate technical documentation and answer custom queries about a codebase.

---

## 🚀 Features

- 🔍 **Query the Knowledge Graph**: Search for functions, variables, files, and configurations from a Neo4j-based code graph.
- 📚 **Context-Aware QA**: Retrieve relevant code context using FAISS and generate explanations using an LLM.
- 📘 **Full Documentation Generation**: Automatically create detailed documentation based on metadata from code.
- 🧠 **LLM-Powered Insights**: Uses Groq's `llama3-70b-8192` model for intelligent, developer-focused documentation generation.

---

## 🛠 Tech Stack

| Layer             | Tools Used                            |
|------------------|----------------------------------------|
| UI               | Streamlit                             |
| Embedding Model  | SentenceTransformers (`all-MiniLM-L6-v2`) |
| Semantic Search  | FAISS                                 |
| Knowledge Graph  | Neo4j                                 |
| LLM              | Groq API with `llama3-70b-8192`        |

---

## 🧩 Project Structure

```
├── app.py                 # Streamlit app (UI + LLM + Graph search)
├── embed_generate.py      # Script to generate and store embeddings in FAISS
├── faiss_functions.bin    # FAISS index for functions
├── faiss_variables.bin    # FAISS index for variables
├── faiss_files.bin        # FAISS index for files
├── faiss_*.pkl            # Metadata for each FAISS index
```

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/repo-doc-generator.git
cd repo-doc-generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Neo4j

Make sure you have Neo4j running locally on `bolt://localhost:7687` and populated with your code graph using `Function`, `Variable`, `File`, `Configuration` nodes.

### 4. Generate Embeddings (Once)

Run the script to generate FAISS indexes:

```bash
python embed_generate.py
```

### 5. Run the App

```bash
streamlit run app.py
```

---

## 🔐 Environment Variables

Set your Groq API key inside `app.py`:

```python
client = Groq(api_key="your_groq_api_key")
```

---

## 🧠 How it Works

1. **Neo4j Graph Querying**:
   - Fetches all nodes (functions, variables, files, configurations) related to the user query.

2. **FAISS Retrieval**:
   - Matches semantically similar items using vector search on pre-computed embeddings.

3. **Groq LLM**:
   - Uses retrieved context to generate answers or full documentation.

---

## 📷 UI Preview

> *Add screenshots or gifs of the Streamlit UI here*

---

## 📃 License

MIT License. Feel free to use and modify!

---

Let me know if you want a shorter version or if you'd like to publish this to Hugging Face or Streamlit Cloud!
