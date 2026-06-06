import os
import json
import re
from pathlib import Path

def analyze_repo():
    repo_data = {
        "files": [],
        "directories": [],
        "dependencies": [],
        "frameworks": [],
        "stats": {
            "html_files": 0,
            "css_files": 0,
            "js_files": 0
        }
    }

    root_dir = Path(".")

    # Analyze files and directories
    for filepath in root_dir.rglob("*"):
        if ".git" in filepath.parts or ".github" in filepath.parts or "docs" in filepath.parts:
            continue

        if filepath.is_file():
            rel_path = str(filepath.relative_to(root_dir))
            repo_data["files"].append(rel_path)

            if rel_path.endswith('.html'):
                repo_data["stats"]["html_files"] += 1
                analyze_html(filepath, repo_data)
            elif rel_path.endswith('.css'):
                repo_data["stats"]["css_files"] += 1
            elif rel_path.endswith('.js'):
                repo_data["stats"]["js_files"] += 1

        elif filepath.is_dir():
            repo_data["directories"].append(str(filepath.relative_to(root_dir)))

    # Save output
    os.makedirs("docs", exist_ok=True)
    with open("docs/repo_analysis.json", "w") as f:
        json.dump(repo_data, f, indent=2)

    print("Repository analysis complete. Output saved to docs/repo_analysis.json")

def analyze_html(filepath, repo_data):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find links to css
    css_links = re.findall(r'<link[^>]*href="([^"]+\.css)"', content)
    for css in css_links:
        repo_data["dependencies"].append({
            "source": str(filepath),
            "target": css,
            "type": "css_link"
        })

    # Find script tags
    js_scripts = re.findall(r'<script[^>]*src="([^"]+\.js)"', content)
    for js in js_scripts:
        repo_data["dependencies"].append({
            "source": str(filepath),
            "target": js,
            "type": "script_src"
        })

if __name__ == "__main__":
    analyze_repo()
