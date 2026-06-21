#!/usr/bin/env python3
"""
Agentic Developer Craftsmanship — Générateur de site statique
Lit les 10 fichiers .md et génère export/site/index.html
"""

import os
import re
from html import unescape
import shutil
import unicodedata
from pathlib import Path

import markdown

COURSE_DIR = Path(__file__).parent
EXPORT_DIR = COURSE_DIR / "export"
SITE_DIR = EXPORT_DIR / "site"
CSS_DIR = SITE_DIR / "css"
JS_DIR = SITE_DIR / "js"
IMG_DIR = SITE_DIR / "img"

VERSION = "1.3"

CHAPTERS = [
    ("CHAPITRE-01-histoire-ia.md",    "Chapitre 1",    "Mettre à jour les paquets"),
    ("CHAPITRE-02-fondations-llm.md", "Chapitre 2",    "Mettre à jour les paquets"),
    ("CHAPITRE-03-prompt-tool-use.md", "Chapitre 3",   "Phase 2 — Interaction avec les LLMs"),
    ("CHAPITRE-04-architecture-agent.md", "Chapitre 4","Phase 2 — Interaction avec les LLMs"),
    ("CHAPITRE-05-memoire-rag.md",    "Chapitre 5",    "Phase 3 — Mémoire & Collaboration"),
    ("CHAPITRE-06-multi-agent.md",    "Chapitre 6",    "Phase 3 — Mémoire & Collaboration"),
    ("CHAPITRE-07-mcp-standards.md",  "Chapitre 7",    "Phase 4 — Production"),
    ("CHAPITRE-08-cicd-devops.md",    "Chapitre 8",    "Phase 4 — Production"),
    ("CHAPITRE-09-securite.md",       "Chapitre 9",    "Phase 5 — Mise en pratique"),
    ("CHAPITRE-10-opencode-labs.md",  "Chapitre 10",   "Phase 5 — Mise en pratique"),
]

PHASES = [
    ("Phase 1", "Mettre à jour les paquets", "De l'histoire de l'IA aux bases des LLM", "#1e3a5f"),
    ("Phase 2", "Interaction avec les LLMs", "Prompt engineering, tool use et boucle agent", "#2563eb"),
    ("Phase 3", "Mémoire & Collaboration", "RAG, mémoire persistante et systèmes multi-agents", "#059669"),
    ("Phase 4", "Production", "MCP, CI/CD et déploiement professionnel", "#7c3aed"),
    ("Phase 5", "Mise en pratique", "Sécurité et labs opencode complets", "#d97706"),
]

APPENDICES = [
    ("projet/gestion_de_projet/cdc.md",  "Annexe A — Cahier des Charges"),
    (".github/workflows/cicd-projet.yml", "Annexe B.1 — Workflow CI/CD Projet"),
    (".github/workflows/test-agents.yml", "Annexe B.2 — Workflow Tests Agents"),
    (".github/workflows/track-progress.yml", "Annexe B.3 — Workflow Suivi Progression"),
]


def slugify(text):
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

def md_to_html(md_text):
    return markdown.markdown(md_text, extensions=['extra', 'smarty'])

def extract_title(md_content):
    m = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    return m.group(1).strip() if m else ""

def fix_mermaid_html(html):
    html = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        r'<pre class="mermaid">\1</pre>',
        html,
        flags=re.DOTALL
    )
    # Inject edgeLabelBackground into every mermaid %%{init} block
    def inject_edge_label(m):
        block = m.group(0)
        if "'edgeLabelBackground'" not in block and '"edgeLabelBackground"' not in block:
            block = re.sub(
                r'(\s*\}\}\}%%)',
                r",\n  'edgeLabelBackground': '#334155'\1",
                block,
                count=1
            )
        return block
    html = re.sub(
        r'<pre class="mermaid">%%\{init:.*?</pre>',
        inject_edge_label,
        html,
        flags=re.DOTALL
    )
    return html

def add_heading_ids(html):
    used_ids = set()
    def _add_id(m):
        nonlocal used_ids
        tag = m.group(0)
        text = re.sub(r'<[^>]+>', '', tag).strip()
        text = unescape(text)
        text = text.replace('\u2019', "'").replace('\u2018', "'")
        text = text.replace('\u201c', '"').replace('\u201d', '"')
        text = re.sub(r'[\(\)]', '', text)
        hid = slugify(text)
        if hid in used_ids:
            counter = 2
            while f"{hid}-{counter}" in used_ids:
                counter += 1
            hid = f"{hid}-{counter}"
        used_ids.add(hid)
        if 'id="' not in tag:
            tag = tag.replace('<h2', f'<h2 id="{hid}"')
            tag = tag.replace('<h3', f'<h3 id="{hid}"')
        return tag
    return re.sub(r'<h[23][^>]*>.*?</h[23]>', _add_id, html)


def build_prerequisites_html():
    """Extract the 'Prérequis général' section from README.md."""
    readme_path = COURSE_DIR / "README.md"
    if not readme_path.exists():
        return ""

    with open(readme_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find "## Prérequis général" and extract until "## Les 10 chapitres"
    start = end = None
    for i, line in enumerate(lines):
        if line.strip() == "## Prérequis général":
            start = i
        if start is not None and line.strip().startswith("## Les 10 chapitres"):
            end = i
            break
    if start is None:
        return ""
    if end is None:
        end = len(lines)

    prerequis_md = ''.join(lines[start:end])
    # Remove the first h2 (we use our own header)
    prerequis_md = re.sub(r'^##\s+.*$', '', prerequis_md, count=1, flags=re.MULTILINE)

    html = md_to_html(prerequis_md)
    html = fix_mermaid_html(html)
    html = add_heading_ids(html)
    return html


def extract_subheadings(md_content):
    """Extract h2 headings from markdown content, skipping metadata sections."""
    headings = []
    skip_patterns = ['objectifs p', 'prerequis', 'prérequis', 'convention', 'point de depart',
                     'point de départ', 'resultat', 'résultat', 'ou se trouve', 'regle',
                     'règle', 'corrige', 'corrigé', 'annexe', 'objectif']
    for line in md_content.split('\n'):
        line_stripped = line.strip()
        if line_stripped.startswith('## ') and not line_stripped.startswith('### '):
            title = line_stripped[3:].strip()
            title_lower = title.lower()
            if any(p in title_lower for p in skip_patterns):
                continue
            if re.match(r'^\d+\.', title):
                headings.append(title)
    return headings

def build_toc_html(include_prerequis=False):
    parts = []
    chapter_count = 0

    for fname, label, phase in CHAPTERS:
        filepath = COURSE_DIR / fname
        chap_id = slugify(label)

        # Extract subheadings and chapter title
        subheadings = []
        chap_title = label
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
            subheadings = extract_subheadings(md_content)
            title = extract_title(md_content)
            if title:
                chap_title = title

        parts.append(f'<li class="toc-chapter"><a href="#{chap_id}">{chap_title}</a></li>')
        for sh in subheadings:
            if chapter_count == 0 and include_prerequis and sh.startswith("6."):
                parts.append(
                    '<li class="toc-sub"><a href="#prerequis-installation"><span class="toc-sub-text">Mise en place des prérequis</span></a></li>'
                )
            sh_id = slugify(sh)
            parts.append(
                f'<li class="toc-sub"><a href="#{sh_id}">'
                f'<span class="toc-sub-text">{sh}</span></a></li>'
            )

        chapter_count += 1

    parts.append(
        '<li class="toc-chapter toc-phase-app"><a href="#annexe-a-cahier-des-charges">Annexes</a></li>'
    )
    for fname, label in APPENDICES:
        app_id = slugify(label)
        parts.append(
            f'<li class="toc-sub"><a href="#{app_id}"><span class="toc-sub-text">{label}</span></a></li>'
        )

    return '\n'.join(parts)


def build_content_html():
    parts = []

    phase_colors = {
        "Mettre à jour les paquets": "#1e3a5f",
        "Phase 2 — Interaction avec les LLMs": "#2563eb",
        "Phase 3 — Mémoire & Collaboration": "#059669",
        "Phase 4 — Production": "#7c3aed",
        "Phase 5 — Mise en pratique": "#d97706",
    }

    current_phase = None
    phase_num = 0
    chapter_count = 0

    for fname, label, phase in CHAPTERS:
        filepath = COURSE_DIR / fname
        if not filepath.exists():
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()

        title = extract_title(md_content)

        # Phase divider
        if phase and phase != current_phase:
            current_phase = phase
            phase_num += 1
            phase_title = PHASES[phase_num - 1][1]
            phase_desc = PHASES[phase_num - 1][2]
            color = phase_colors.get(phase, "#1e3a5f")
            parts.append(f'''
<section class="phase-divider" style="--phase-color: {color};">
    <div class="phase-badge">Phase {phase_num}</div>
    <h2 class="phase-title">{phase_title}</h2>
    <div class="phase-line"></div>
    <p class="phase-desc">{phase_desc}</p>
</section>
''')

        # Remove first h1
        md_content = re.sub(r'^#\s+.*$', '', md_content, count=1, flags=re.MULTILINE)

        # Split Ch1: theory part before TP, practical part from TP onward
        ch1_theory = None
        ch1_tp = None
        if chapter_count == 0:
            tp_marker = "## 6. Travaux Pratiques"
            tp_pos = md_content.find(tp_marker)
            if tp_pos != -1:
                ch1_theory = md_content[:tp_pos]
                ch1_tp = md_content[tp_pos:]
            else:
                ch1_theory = md_content
            # Strip the Prérequis block from theory (covered by README prerequis section before TP)
            ch1_theory = re.sub(
                r'^## Prérequis\n.*?(?=\n## |\Z)',
                '',
                ch1_theory,
                count=1,
                flags=re.DOTALL | re.MULTILINE
            )

        # Convert to HTML
        if ch1_theory is not None:
            theory_html = md_to_html(ch1_theory)
            theory_html = fix_mermaid_html(theory_html)
            theory_html = add_heading_ids(theory_html)
        else:
            html = md_to_html(md_content)
            html = fix_mermaid_html(html)
            html = add_heading_ids(html)

        if not title:
            title = label

        chap_id = slugify(label)

        # Output Ch1 theory
        if ch1_theory is not None:
            parts.append(f'''
<section class="chapter" id="{chap_id}">
    <div class="chapter-header" style="background: linear-gradient(135deg, #0f172a, {phase_colors.get(phase, '#1e3a5f')});">
        <div class="ch-meta">{phase}</div>
        <h1>{title}</h1>
    </div>
    <div class="chapter-body">
        {theory_html}
    </div>
</section>
''')

            # Insert README prerequis between theory and TP
            prerequis_html = build_prerequisites_html()
            if prerequis_html:
                parts.append(f'''
<section class="chapter" id="prerequis-installation">
    <div class="chapter-header" style="background: linear-gradient(135deg, #0f172a, #059669);">
        <div class="ch-meta">Prérequis</div>
        <h1>Mise en place des prérequis</h1>
    </div>
    <div class="chapter-body">
        {prerequis_html}
    </div>
</section>
''')

            # Output Ch1 TP as a separate section
            if ch1_tp:
                tp_html = md_to_html(ch1_tp)
                tp_html = fix_mermaid_html(tp_html)
                tp_html = add_heading_ids(tp_html)
                parts.append(f'''
<section class="chapter" id="chapitre-1-tp">
    <div class="chapter-header" style="background: linear-gradient(135deg, #0f172a, {phase_colors.get(phase, '#1e3a5f')});">
        <div class="ch-meta">{phase} — Travaux Pratiques</div>
        <h1>{title} — TP</h1>
    </div>
    <div class="chapter-body">
        {tp_html}
    </div>
</section>
''')
        else:
            # Normal chapters
            parts.append(f'''
<section class="chapter" id="{chap_id}">
    <div class="chapter-header" style="background: linear-gradient(135deg, #0f172a, {phase_colors.get(phase, '#1e3a5f')});">
        <div class="ch-meta">{phase}</div>
        <h1>{title}</h1>
    </div>
    <div class="chapter-body">
        {html}
    </div>
</section>
''')

        chapter_count += 1

    # Appendices
    for fname, label in APPENDICES:
        filepath = COURSE_DIR / fname
        if not filepath.exists():
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if fname.endswith('.yml'):
            md_content = f"```yaml\n{content}\n```"
        else:
            md_content = content

        html = md_to_html(md_content)
        app_id = slugify(label)

        parts.append(f'''
<section class="chapter appendix" id="{app_id}">
    <div class="chapter-header" style="background: linear-gradient(135deg, #0f172a, #4c1d95);">
        <div class="ch-meta">Annexe</div>
        <h1>{label}</h1>
    </div>
    <div class="chapter-body">
        {html}
    </div>
</section>
''')

    return '\n'.join(parts)


def build_site():
    print("=" * 60)
    print("Agentic Developer Craftsmanship — Générateur de site")
    print("=" * 60)

    SITE_DIR.mkdir(parents=True, exist_ok=True)
    CSS_DIR.mkdir(parents=True, exist_ok=True)
    JS_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.joinpath("pdf").mkdir(parents=True, exist_ok=True)

    # Copy assets
    logo_src = COURSE_DIR / "logo.jpeg"
    if logo_src.exists():
        shutil.copy(logo_src, IMG_DIR / "logo.jpeg")

    # Copy CSS files (they already exist at their target location)
    if not (CSS_DIR / "style.css").exists():
        print("  WARNING: style.css not found at", CSS_DIR)

    # Build content
    print("\n[1/2] Conversion des chapitres...")
    content_html = build_content_html()
    toc_html = build_toc_html(include_prerequis=True)

    # Build final HTML
    print("\n[2/2] Génération de l'HTML...")

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agentic Developer Craftsmanship — v{VERSION}</title>
<link rel="stylesheet" href="css/style.css">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
</head>
<body>

<div class="layout">

<aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
        <img src="img/logo.jpeg" alt="Sup Devinci Rennes" class="sidebar-logo" />
        <div class="sidebar-title">Agentic Developer<br/>Craftsmanship</div>
        <div class="sidebar-author">Youghourta Merabtène</div>
        <div class="sidebar-version">v{VERSION}</div>
    </div>
    <div class="sidebar-toggle" id="sidebar-toggle">&times;</div>
    <nav class="sidebar-nav">
        <ul class="toc">
            {toc_html}
        </ul>
    </nav>
    <div class="sidebar-footer">
        <a href="#" class="sidebar-home">&#8593; Haut de page</a>
    </div>
</aside>

<button class="menu-btn" id="menu-btn">&#9776;</button>

<main class="content" id="content">

<section class="toc-section" id="sommaire">
    <div class="toc-section-header">
        <h1>Table des matières</h1>
        <p class="toc-subtitle">Agentic Developer Craftsmanship &mdash; v{VERSION}</p>
        <p class="toc-author">Youghourta Merabtène &mdash; Sup Devinci Rennes</p>
    </div>
    <ul class="toc-section-list">
        {toc_html}
    </ul>
</section>

{content_html}

<footer class="site-footer">
    <div class="footer-inner">
        <p><strong>Agentic Developer Craftsmanship</strong> — v{VERSION}</p>
        <p>Auteur : Youghourta Merabtène — Sup Devinci Rennes</p>
        <p>Ce cours est 100% open-source.</p>
    </div>
</footer>

</main>
</div>

<script>
mermaid.initialize({{
    theme: 'base',
    themeVariables: {{
        primaryColor: '#1e3a5f',
        primaryTextColor: '#fff',
        lineColor: '#2563eb',
        secondaryColor: '#f1f5f9',
        tertiaryColor: '#eef2ff',
        edgeLabelBackground: '#334155',
    }}
}});
mermaid.run({{ nodes: document.querySelectorAll('.mermaid') }});
hljs.highlightAll();
</script>
<script src="js/site.js"></script>
</body>
</html>
'''

    index_path = SITE_DIR / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size = index_path.stat().st_size / 1024
    print(f"  index.html généré : {index_path} ({size:.0f} Ko)")

    print(f"\n✅ Site prêt dans {SITE_DIR}")
    print(f"   Ouvrir : file://{SITE_DIR / 'index.html'}")


if __name__ == '__main__':
    build_site()
