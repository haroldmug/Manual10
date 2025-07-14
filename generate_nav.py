#!/usr/bin/env python3
import os
from ruamel.yaml import YAML

# ──────────────────────────────────────────────────────────────────────────────
# Adjust only if your layout differs:
DOCS_ROOT = 'docs'         # where all subject subfolders live
MKDOCS_YML = 'mkdocs.yml'  # your MkDocs config
# ──────────────────────────────────────────────────────────────────────────────

yaml = YAML()
yaml.preserve_quotes = True

# 1) Load your existing mkdocs.yml
with open(MKDOCS_YML, 'r', encoding='utf-8') as fp:
    config = yaml.load(fp)

# 2) Build a fresh `nav:` list
new_nav = []

# 2a) Main landing page
new_nav.append({'Manual': 'index.md'})

# 2b) One collapsible entry per subject, containing only that subject's chapter files
for subject in sorted(os.listdir(DOCS_ROOT)):
    subj_path = os.path.join(DOCS_ROOT, subject)
    if not os.path.isdir(subj_path):
        continue

    # Collect all .md except index.md
    chapters = [
        fn for fn in os.listdir(subj_path)
        if fn.lower().endswith('.md') and fn.lower() != 'index.md'
    ]

    # Sort by leading number (files without a number go last)
    def sort_key(fn):
        parts = fn.split('.', 1)
        return (int(parts[0]), fn.lower()) if parts[0].isdigit() else (float('inf'), fn.lower())

    chapters.sort(key=sort_key)

    # Prepend folder name so MkDocs can resolve the path
    links = [f"{subject}/{chapter}" for chapter in chapters]

    # Add a single nav entry: subject name → list of chapters
    new_nav.append({subject: links})

# 3) Inject it back into config and write out
config['nav'] = new_nav

with open(MKDOCS_YML, 'w', encoding='utf-8') as fp:
    yaml.dump(config, fp)

print("mkdocs.yml updated: left-nav now shows each subject once, with its chapters nested.")
