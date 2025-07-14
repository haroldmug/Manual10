#!/usr/bin/env python3
import os
import re

# Adjust if your docs folder has a different name
DOCS_ROOT = 'docs'

def sorted_chapters(folder_path):
    """
    List all .md files except index.md, sorted by their leading number.
    """
    files = [
        fn for fn in os.listdir(folder_path)
        if fn.lower().endswith('.md') and fn.lower() != 'index.md'
    ]
    def sort_key(fn):
        m = re.match(r'^(\d+)', fn)
        return int(m.group(1)) if m else fn.lower()
    return sorted(files, key=sort_key)

def make_landing(subject):
    """
    Overwrite docs/<subject>/index.md with:
      # <Subject>
      [← Return to Manual](../index.md)

      ## Chapters
      - [1. Foo Bar](./1.%20Foo%20Bar.md)
      - [2. Baz](./2.%20Baz.md)
    """
    subj_dir = os.path.join(DOCS_ROOT, subject)
    chapters = sorted_chapters(subj_dir)

    lines = [
        f"# {subject}",
        "",
        "[← Return to Manual](../index.md)",
        "",
        "## Chapters",
        ""
    ]

    for chap in chapters:
        title = chap[:-3]  # strip the “.md”
        # encode spaces so MkDocs recognizes the link in source
        url   = chap.replace(' ', '%20')
        lines.append(f"- [{title}](./{url})")

    lines.append("")  # final newline

    target = os.path.join(subj_dir, 'index.md')
    with open(target, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    for entry in sorted(os.listdir(DOCS_ROOT)):
        path = os.path.join(DOCS_ROOT, entry)
        if os.path.isdir(path):
            make_landing(entry)
    print("Landing pages generated.")
