import os
import json
from jinja2 import Template

def update_readme():
    with open(".github/templates/README.tmpl.md", "r") as f:
        template_content = f.read()

    template = Template(template_content)

    with open("docs/repo_analysis.json", "r") as f:
        repo_data = json.load(f)

    with open("docs/diagrams/architecture.mermaid", "r") as f:
        arch_mermaid = f.read()

    with open("docs/diagrams/dependencies.mermaid", "r") as f:
        deps_mermaid = f.read()

    rendered_readme = template.render(
        stats=repo_data.get("stats", {}),
        arch_mermaid=arch_mermaid,
        deps_mermaid=deps_mermaid,
        files=repo_data.get("files", [])
    )

    with open("README.md", "w") as f:
        f.write(rendered_readme)

    print("README.md updated successfully.")

if __name__ == "__main__":
    update_readme()
