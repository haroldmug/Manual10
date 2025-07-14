#!/usr/bin/env python3
import os
import re
from urllib.parse import quote

# Where your topic folders live
DOCS_ROOT = 'docs'

def sorted_chapters(folder_path):
    """
    Return all .md files except index.md, sorted by
    their leading number (if present), otherwise lexically.
    """
    files = [
        fn for fn in os.listdir(folder_path)
        if fn.lower().endswith('.md') and fn.lower() != 'index.md'
    ]
    def keyfn(fn):
        m = re.match(r'^(\d+)', fn)
        return (int(m.group(1)), fn.lower()) if m else (float('inf'), fn.lower())
    return sorted(files, key=keyfn)

def make_landing(subject):
    subject_dir = os.path.join(DOCS_ROOT, subject)
    chapters    = sorted_chapters(subject_dir)

    lines = [
        f"# {subject}",
        "",
        "[← Return to Manual](../index.md)",
        "",
        "## Chapters",
        ""
    ]

    for chap in chapters:
        title = chap[:-3]             # strip “.md”
        # percent-encode spaces/special chars, then add trailing slash
        url   = quote(title) + '/'
        lines.append(f"- [{title}](./{url})")

    lines.append("")  # final newline

    out_path = os.path.join(subject_dir, 'index.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    # regenerate landing page for each folder in docs/
    for entry in sorted(os.listdir(DOCS_ROOT)):
        path = os.path.join(DOCS_ROOT, entry)
        if os.path.isdir(path):
            make_landing(entry)
    print("Landing pages regenerated.")
