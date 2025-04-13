
---

# 📄 Codebase Documentation Generator

A lightweight tool to **generate documentation** and **answer technical questions** about any codebase using:

- 🌐 **Neo4j** for code graph storage  
- 🔍 **FAISS** for semantic code search  
- 🧠 **Sentence Transformers** for embeddings  
- ⚡ **Groq (LLaMA 3)** for fast and accurate LLM responses  

---

## 🗂 Directory Structure

```
Directory structure:
└── amanpreet0kaur-codebase-documentation-generator/
    ├── README.md
    ├── requirements.txt
    └── app/
        ├── app2.py
        ├── embed.py
        ├── faiss_files.bin
        ├── faiss_files.pkl
        ├── faiss_functions.bin
        ├── faiss_functions.pkl
        ├── faiss_variables.bin
        ├── faiss_variables.pkl
        └── graph.py

```

---

## 🚀 Features

- 🔍 **Search across functions, variables, files**
- 🧠 **Query-aware explanations via LLM**
- 📘 **Autogenerate full documentation**
- ⚡️ Fast and scalable using FAISS + Groq

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/amanpreet0kaur-codebase-documentation-generator.git
cd amanpreet0kaur-codebase-documentation-generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```



### 3. Setup Neo4j

Ensure you have Neo4j running locally:

```bash
bolt://localhost:7687
```

Graph nodes expected:  
- `Function`, `Variable`, `File`, `Configuration`

Update credentials in `graph.py` and `embed.py` if needed:

```python
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "your_password"
```

### 4. Generate Embeddings + FAISS Index

```bash
python embed.py
```

This generates:
- `faiss_*.bin` (FAISS indexes)
- `faiss_*.pkl` (metadata)

### 5. Launch the App

```bash
streamlit run app2.py
```

---

## 🔐 API Configuration

Add your [Groq API Key](https://console.groq.com/) in `app2.py`:

```python
from groq import Groq
client = Groq(api_key="your_groq_api_key")
```

---

## 📘 How It Works

1. **embed.py**  
   → Connects to Neo4j  
   → Extracts functions, variables, files  
   → Creates SentenceTransformer embeddings  
   → Saves to FAISS + metadata files  

2. **app2.py**  
   → Takes user queries  
   → Searches both Neo4j & FAISS  
   → Passes relevant context to LLM  
   → Returns generated explanation or full documentation  

---

## 🧠 Powered By

- **Neo4j** – Code relationship graph  
- **FAISS** – Fast Approximate Nearest Neighbors  
- **Sentence Transformers** – Semantic search  
- **Groq + LLaMA 3** – LLM-based responses and documentation  

---


## 📷 UI Preview
QUERY SEARCH:
![image](https://github.com/user-attachments/assets/1128793c-5eb2-481c-b0a2-d88c1c29429b)
DOCUMENTATION GENERATION:
![image](https://github.com/user-attachments/assets/a889c50c-034e-472c-a397-96fa5e125571)



---






