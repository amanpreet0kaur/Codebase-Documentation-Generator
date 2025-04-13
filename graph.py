from neo4j import GraphDatabase
import ast
import os
import re

# ✅ Neo4j Connection Setup
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "12345678"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

### ✅ Extract Components from Python Files
def parse_python(file_path):
    """Extract functions, classes, imports, and variables from a Python file"""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    functions, classes, imports, variables = [], [], [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    variables.append(target.id)
                elif isinstance(target, ast.Tuple):
                    variables.extend([elt.id for elt in target.elts if isinstance(elt, ast.Name)])

    return functions, classes, imports, variables

### ✅ Extract Components from JavaScript Files
def parse_javascript(file_path):
    """Extract functions, classes, imports, and variables from JavaScript files"""
    functions, classes, imports, variables = [], [], [], []

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    function_pattern = re.findall(r"function\s+(\w+)\s*\(", code)
    class_pattern = re.findall(r"class\s+(\w+)", code)
    import_pattern = re.findall(r"import\s+.*\s+from\s+['\"]([\w\-/]+)['\"]", code)
    variable_pattern = re.findall(r"var\s+(\w+)|let\s+(\w+)|const\s+(\w+)", code)

    functions.extend(function_pattern)
    classes.extend(class_pattern)
    imports.extend(import_pattern)

    for match in variable_pattern:
        variables.extend([v for v in match if v])

    return functions, classes, imports, variables

### ✅ Extract Components from CSS Files
def parse_css(file_path):
    """Extract CSS classes and IDs"""
    css_classes, css_ids = [], []

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    css_classes.extend(re.findall(r"\.(\w+)", code))
    css_ids.extend(re.findall(r"#(\w+)", code))

    return css_classes, css_ids

### ✅ Store Everything in Neo4j
def store_in_neo4j(repo_path):
    """Store directory structure and file contents into Neo4j"""
    with driver.session() as session:
        for root, dirs, files in os.walk(repo_path):
            relative_root = root.replace(repo_path, "").strip("\\/")
            parent_dir = os.path.dirname(relative_root).strip("\\/")

            # Directory node
            if relative_root:
                session.run("MERGE (d:Directory {name: $name})", name=relative_root)
                if parent_dir:
                    session.run("""
                        MATCH (parent:Directory {name: $parent})
                        WITH parent
                        MATCH (child:Directory {name: $child})
                        MERGE (parent)-[:SUBDIRECTORY_OF]->(child)
                    """, parent=parent_dir, child=relative_root)

            for file in files:
                file_path = os.path.join(root, file)
                file_name = file_path.replace(repo_path, "").strip("\\/")

                # File node
                session.run("MERGE (f:File {name: $name})", name=file_name)
                if relative_root:
                    session.run("""
                        MATCH (dir:Directory {name: $dir})
                        WITH dir
                        MATCH (f:File {name: $file})
                        MERGE (dir)-[:CONTAINS]->(f)
                    """, dir=relative_root, file=file_name)

                # Python Files
                if file.endswith(".py"):
                    funcs, classes, imports, variables = parse_python(file_path)

                    for func in funcs:
                        session.run("""
                            MERGE (fn:Function {name: $func})
                            WITH fn
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:CONTAINS]->(fn)
                        """, func=func, file=file_name)

                    for cls in classes:
                        session.run("""
                            MERGE (c:Class {name: $cls})
                            WITH c
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:CONTAINS]->(c)
                        """, cls=cls, file=file_name)

                    for imp in imports:
                        session.run("""
                            MERGE (i:Import {name: $imp})
                            WITH i
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:IMPORTS]->(i)
                        """, imp=imp, file=file_name)

                    for var in variables:
                        session.run("""
                            MERGE (v:Variable {name: $var})
                            WITH v
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:DECLARES]->(v)
                        """, var=var, file=file_name)

                # JavaScript Files
                elif file.endswith(".js"):
                    funcs, classes, imports, variables = parse_javascript(file_path)

                    for func in funcs:
                        session.run("""
                            MERGE (fn:Function {name: $func})
                            WITH fn
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:CONTAINS]->(fn)
                        """, func=func, file=file_name)

                    for cls in classes:
                        session.run("""
                            MERGE (c:Class {name: $cls})
                            WITH c
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:CONTAINS]->(c)
                        """, cls=cls, file=file_name)

                    for imp in imports:
                        session.run("""
                            MERGE (i:Import {name: $imp})
                            WITH i
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:IMPORTS]->(i)
                        """, imp=imp, file=file_name)

                    for var in variables:
                        session.run("""
                            MERGE (v:Variable {name: $var})
                            WITH v
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:DECLARES]->(v)
                        """, var=var, file=file_name)

                # CSS Files
                elif file.endswith(".css"):
                    css_classes, css_ids = parse_css(file_path)

                    for cls in css_classes:
                        session.run("""
                            MERGE (c:CSSClass {name: $cls})
                            WITH c
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:STYLES]->(c)
                        """, cls=cls, file=file_name)

                    for cid in css_ids:
                        session.run("""
                            MERGE (id:CSSID {name: $cid})
                            WITH id
                            MATCH (f:File {name: $file})
                            MERGE (f)-[:STYLES]->(id)
                        """, cid=cid, file=file_name)

        print("✅ Data successfully stored in Neo4j!")

### 🚀 Run It
repo_path = r"E:\foss"  # Change this to your repo path
store_in_neo4j(repo_path)
