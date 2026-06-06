import json
import os

def generate_diagrams():
    with open("docs/repo_analysis.json", "r") as f:
        repo_data = json.load(f)

    os.makedirs("docs/diagrams", exist_ok=True)

    # Generate Dependency Graph
    mermaid_deps = "graph TD;\n"
    for dep in repo_data.get("dependencies", []):
        source = dep["source"].replace("\\", "/")
        target = dep["target"].replace("\\", "/")
        mermaid_deps += f'    "{source}" --> "{target}";\n'

    with open("docs/diagrams/dependencies.mermaid", "w") as f:
        f.write(mermaid_deps)

    # Generate Architecture Diagram (Simplified)
    mermaid_arch = """graph LR;
    subgraph Frontend
        HTML[HTML Pages]
        CSS[Stylesheets]
        JS[JavaScript Scripts]
    end
    HTML --> CSS
    HTML --> JS
    """

    with open("docs/diagrams/architecture.mermaid", "w") as f:
        f.write(mermaid_arch)

    print("Diagrams generated in docs/diagrams/")

if __name__ == "__main__":
    generate_diagrams()
