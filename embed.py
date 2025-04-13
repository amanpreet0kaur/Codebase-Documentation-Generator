from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from neo4j import GraphDatabase

# ✅ Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"  # Ensure Neo4j is running on this port
NEO4J_USER = "neo4j"  # Default user
NEO4J_PASS = "12345678"  # Replace with your actual password

model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# ✅ Store data
functions, variables, files = [], [], []
function_texts, variable_texts, file_texts = [], [], []

with driver.session() as session:
    # ✅ Extract functions
    results = session.run("MATCH (fn:Function) RETURN fn.name")
    for record in results:
        functions.append(record["fn.name"])
        function_texts.append(record["fn.name"])  # Can add docstrings if available

    # ✅ Extract variables
    results = session.run("MATCH (var:Variable) RETURN var.name")
    for record in results:
        variables.append(record["var.name"])
        variable_texts.append(record["var.name"])  # Can add additional metadata

    # ✅ Extract files
    results = session.run("MATCH (f:File) RETURN f.name")
    for record in results:
        files.append(record["f.name"])
        file_texts.append(record["f.name"])  # Can add file type if needed

# ✅ Compute embeddings
function_embeddings = model.encode(function_texts)
variable_embeddings = model.encode(variable_texts)
file_embeddings = model.encode(file_texts)

# ✅ Convert to numpy arrays
function_embeddings = np.array(function_embeddings)
variable_embeddings = np.array(variable_embeddings)
file_embeddings = np.array(file_embeddings)

# ✅ Store in FAISS
index_functions = faiss.IndexFlatL2(function_embeddings.shape[1])
index_functions.add(function_embeddings)

index_variables = faiss.IndexFlatL2(variable_embeddings.shape[1])
index_variables.add(variable_embeddings)

index_files = faiss.IndexFlatL2(file_embeddings.shape[1])
index_files.add(file_embeddings)

# ✅ Save metadata
with open("faiss_functions.pkl", "wb") as f:
    pickle.dump(functions, f)

with open("faiss_variables.pkl", "wb") as f:
    pickle.dump(variables, f)

with open("faiss_files.pkl", "wb") as f:
    pickle.dump(files, f)

# ✅ Save FAISS indexes
faiss.write_index(index_functions, "faiss_functions.bin")
faiss.write_index(index_variables, "faiss_variables.bin")
faiss.write_index(index_files, "faiss_files.bin")

print("✅ FAISS embeddings stored for functions, variables, and files.")
