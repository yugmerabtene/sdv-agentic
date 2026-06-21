#!/usr/bin/env python3
"""
Agentic Developer Craftsmanship — Générateur PDF v1.3
Convertit les 12 fichiers .md du cours en un PDF professionnel.
"""

import os
import re
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

# ─── Configuration ───────────────────────────────────────────────────────────

COURSE_DIR = Path("/home/yug/Documents/Agentic-Developer-Craftsmanship")
VERSION = "1.3"
OUTPUT_PDF = COURSE_DIR / f"Agentic-Developer-Craftsmanship-v{VERSION}.pdf"
LOGO_PATH = COURSE_DIR / "logo.jpeg"

CHAPTERS = [
    ("README.md",                     "Préface",         None),
    ("CHAPITRE-01-histoire-ia.md",    "Chapitre 1",      "Phase 1 — Fondamentaux"),
    ("CHAPITRE-02-fondations-llm.md", "Chapitre 2",      "Phase 1 — Fondamentaux"),
    ("CHAPITRE-03-prompt-tool-use.md", "Chapitre 3",     "Phase 2 — Interaction avec les LLMs"),
    ("CHAPITRE-04-architecture-agent.md", "Chapitre 4",  "Phase 2 — Interaction avec les LLMs"),
    ("CHAPITRE-05-memoire-rag.md",    "Chapitre 5",      "Phase 3 — Mémoire & Collaboration"),
    ("CHAPITRE-06-multi-agent.md",    "Chapitre 6",      "Phase 3 — Mémoire & Collaboration"),
    ("CHAPITRE-07-mcp-standards.md",  "Chapitre 7",      "Phase 4 — Production"),
    ("CHAPITRE-08-cicd-devops.md",    "Chapitre 8",      "Phase 4 — Production"),
    ("CHAPITRE-09-securite.md",       "Chapitre 9",      "Phase 5 — Mise en pratique"),
    ("CHAPITRE-10-opencode-labs.md",  "Chapitre 10",     "Phase 5 — Mise en pratique"),
]

APPENDICES = [
    ("projet/gestion_de_projet/cdc.md",  "Annexe A — Cahier des Charges"),
    (".github/workflows/cicd-projet.yml", "Annexe B.1 — Workflow CI/CD Projet"),
    (".github/workflows/test-agents.yml", "Annexe B.2 — Workflow Tests Agents"),
    (".github/workflows/track-progress.yml", "Annexe B.3 — Workflow Suivi Progression"),
]

# ─── CSS Stylesheet ──────────────────────────────────────────────────────────

CSS_STYLES = """
@page {
    size: A4;
    margin: 2.5cm 2.5cm 3cm 2.5cm;
    @bottom-center {
        content: counter(page);
        font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
        font-size: 9pt;
        color: #64748b;
    }
    @top-left {
        content: string(chapter);
        font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
    }
    @top-right {
        content: string(phase);
        font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
    }
}

@page cover {
    margin: 0;
    @bottom-center { content: none; }
    @top-left { content: none; }
    @top-right { content: none; }
}

@page toc {
    @top-left { content: none; }
    @top-right { content: none; }
}

@page chapter-first {
    @top-left { content: none; }
    @top-right { content: none; }
}

* { box-sizing: border-box; }

html {
    font-family: 'DejaVu Serif', 'Liberation Serif', serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1e293b;
}

body {
    margin: 0;
    padding: 0;
}

/* ─── Cover Page ───────────────────────────────────────────────────── */

.cover-page {
    page: cover;
    break-after: page;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 50%, #1e3a5f 100%);
    color: #ffffff;
    text-align: center;
    padding: 4cm;
    position: relative;
    overflow: hidden;
}

.cover-page::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(37, 99, 235, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(37, 99, 235, 0.10) 0%, transparent 50%);
}

.cover-logo {
    margin-bottom: 3cm;
    position: relative;
}
.cover-logo img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 3px solid rgba(255,255,255,0.3);
    padding: 4px;
}

.cover-line {
    width: 80px;
    height: 3px;
    background: #3b82f6;
    margin: 1.5cm auto;
    position: relative;
}

.cover-title {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 26pt;
    font-weight: 700;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin: 0 0 0.5cm 0;
    position: relative;
}

.cover-subtitle {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 13pt;
    font-weight: 300;
    color: #93c5fd;
    margin: 0 0 2cm 0;
    position: relative;
    line-height: 1.4;
}

.cover-meta {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 10pt;
    color: #94a3b8;
    margin-top: auto;
    position: relative;
    line-height: 1.8;
}
.cover-meta strong {
    color: #cbd5e1;
}

.cover-version {
    position: absolute;
    bottom: 1.5cm;
    right: 2.5cm;
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    color: #475569;
    background: rgba(30, 41, 59, 0.8);
    padding: 4px 12px;
    border-radius: 4px;
}

/* ─── Table of Contents ────────────────────────────────────────────── */

.toc-page {
    page: toc;
    break-after: page;
    padding: 0;
}

.toc-title {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 20pt;
    font-weight: 700;
    color: #1e3a5f;
    margin: 0 0 0.8cm 0;
    padding-bottom: 0.3cm;
    border-bottom: 3px solid #1e3a5f;
}

.toc-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.toc-item {
    padding: 6pt 0;
    border-bottom: 1px dotted #e2e8f0;
    display: flex;
    justify-content: space-between;
}

.toc-item a {
    color: #1e293b;
    text-decoration: none;
    flex: 1;
}

.toc-item .toc-page-num {
    color: #64748b;
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
}

.toc-phase {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    font-weight: 600;
    color: #3b82f6;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding-top: 10pt;
}

.toc-chapter {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-weight: 500;
    padding-left: 14pt;
}

.toc-appendix {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-weight: 600;
    color: #1e3a5f;
    padding-top: 10pt;
}

/* ─── Chapter Styles ───────────────────────────────────────────────── */

.chapter-container {
    page-break-before: always;
    string-set: chapter attr(data-chapter);
}

.chapter-container.phase-start {
    string-set: chapter attr(data-chapter);
}

.chapter-header {
    background: linear-gradient(135deg, #1e3a5f, #2563eb);
    color: #ffffff;
    padding: 1.2cm 1.5cm;
    margin: 0 0 0.8cm 0;
    border-radius: 0;
}

.chapter-header h1 {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 18pt;
    font-weight: 700;
    margin: 0;
    line-height: 1.3;
}

.chapter-header .chapter-meta {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    color: #93c5fd;
    margin-top: 6pt;
}

/* ─── Phase divider ────────────────────────────────────────────────── */

.phase-divider {
    page-break-before: always;
    break-before: page;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60vh;
    text-align: center;
}

.phase-divider h1 {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 22pt;
    font-weight: 700;
    color: #1e3a5f;
    margin: 0;
}

.phase-divider .phase-line {
    width: 60px;
    height: 3px;
    background: #2563eb;
    margin: 0.6cm auto;
}

.phase-divider .phase-desc {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 11pt;
    color: #64748b;
}

/* ─── Appendix styles ──────────────────────────────────────────────── */

.appendix-container {
    page-break-before: always;
    string-set: chapter "Annexes";
    string-set: phase "Appendices";
}

.appendix-header {
    background: #1e3a5f;
    color: #ffffff;
    padding: 0.8cm 1.2cm;
    margin: 0 0 0.8cm 0;
}

.appendix-header h1 {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 16pt;
    font-weight: 700;
    margin: 0;
}

.appendix-header .appendix-meta {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    color: #94a3b8;
    margin-top: 4pt;
}

/* ─── Typography ───────────────────────────────────────────────────── */

h1, h2, h3, h4, h5, h6 {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    color: #1e3a5f;
    margin: 0.6cm 0 0.3cm 0;
    line-height: 1.3;
}

h2 {
    font-size: 14pt;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 4pt;
}

h3 {
    font-size: 12pt;
    color: #2563eb;
}

h4 { font-size: 11pt; }
h5 { font-size: 10.5pt; }
h6 { font-size: 10pt; color: #64748b; }

p { margin: 0 0 0.35cm 0; text-align: justify; }

a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }

strong { color: #0f172a; }
em { font-style: italic; }

/* ─── Code Blocks ──────────────────────────────────────────────────── */

pre {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #2563eb;
    border-radius: 4px;
    padding: 10pt 12pt;
    font-family: 'DejaVu Sans Mono', 'Liberation Mono', monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
    margin: 0.35cm 0;
}

code {
    font-family: 'DejaVu Sans Mono', 'Liberation Mono', monospace;
    font-size: 9pt;
    background: #f1f5f9;
    padding: 1pt 4pt;
    border-radius: 3px;
    color: #1e293b;
}

pre code {
    background: none;
    padding: 0;
    font-size: inherit;
    color: inherit;
}

/* ─── Inline code in headers ───────────────────────────────────────── */

h1 code, h2 code, h3 code, h4 code {
    font-size: inherit;
}

/* ─── Tables ───────────────────────────────────────────────────────── */

table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.4cm 0;
    font-size: 9.5pt;
}

th {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    background: #1e3a5f;
    color: #ffffff;
    padding: 6pt 8pt;
    text-align: left;
    font-weight: 600;
}

td {
    padding: 5pt 8pt;
    border-bottom: 1px solid #e2e8f0;
}

tr:nth-child(even) td {
    background: #f8fafc;
}

tr:hover td {
    background: #eef2ff;
}

/* ─── Blockquotes / Admonitions ────────────────────────────────────── */

blockquote {
    margin: 0.4cm 0;
    padding: 8pt 12pt;
    border-left: 4px solid #2563eb;
    background: #f0f4ff;
    border-radius: 0 4px 4px 0;
}

blockquote p { margin: 0; }

blockquote strong:first-child {
    color: #1e3a5f;
    text-transform: uppercase;
    font-size: 8pt;
    letter-spacing: 0.5px;
}

/* ─── Horizontal Rules ─────────────────────────────────────────────── */

hr {
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 0.6cm 0;
}

/* ─── Lists ────────────────────────────────────────────────────────── */

ul, ol {
    margin: 0.2cm 0;
    padding-left: 1.2cm;
}

li { margin-bottom: 3pt; }

/* ─── Images ───────────────────────────────────────────────────────── */

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0.4cm auto;
}

/* ─── Small print / meta ───────────────────────────────────────────── */

.small {
    font-size: 8.5pt;
    color: #64748b;
}
"""


# ─── Helpers ─────────────────────────────────────────────────────────────────

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def extract_mermaid_blocks(md_content):
    """Extract all mermaid code blocks with their positions."""
    pattern = r'```mermaid\n(.*?)```'
    blocks = []
    for match in re.finditer(pattern, md_content, re.DOTALL):
        blocks.append({
            'start': match.start(),
            'end': match.end(),
            'code': match.group(1).strip(),
        })
    return blocks

def extract_title(md_content):
    """Extract first h1 title from markdown."""
    m = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    return m.group(1).strip() if m else ""

def strip_code_fences(text):
    """Remove surrounding code fence markers."""
    text = re.sub(r'^```\w*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    return text


# ─── Mermaid Rendering ───────────────────────────────────────────────────────

def render_mermaid_blocks(md_content, output_dir, image_dir, counter=[0]):
    """Replace mermaid code blocks with image references. Returns modified content."""
    blocks = extract_mermaid_blocks(md_content)
    if not blocks:
        return md_content

    # Process in reverse order to preserve positions
    result = md_content
    for block in reversed(blocks):
        counter[0] += 1
        seq = counter[0]
        mmd_file = output_dir / f"diagram-{seq:03d}.mmd"
        png_file = image_dir / f"diagram-{seq:03d}.png"
        rel_path = png_file.resolve()

        with open(mmd_file, 'w', encoding='utf-8') as f:
            f.write(block['code'])

        print(f"  Rendu mermaid #{seq}...")
        subprocess.run([
            'mmdc',
            '-i', str(mmd_file),
            '-o', str(png_file),
            '-b', 'transparent',
            '--width', '800',
            '--height', '600',
        ], capture_output=True, text=True, timeout=60)

        img_tag = f'\n\n![Diagramme {seq}]({rel_path})\n\n'
        before = result[:block['start']]
        after = result[block['end']:]
        result = before + img_tag + after

    return result


# ─── Markdown → HTML conversion ─────────────────────────────────────────────

def md_to_html(md_text, extensions=None):
    if extensions is None:
        extensions = [
            'extra',           # tables, footnotes, etc.
            'codehilite',      # syntax highlighting
            'toc',             # table of contents
            'smarty',          # smart quotes, dashes
            'nl2br',           # newline to <br>
        ]
    return markdown.markdown(md_text, extensions=extensions)


# ─── Build combined HTML ─────────────────────────────────────────────────────

def build_html():
    """Build the complete HTML document."""
    temp_dir = Path(tempfile.mkdtemp(prefix='pdf_build_'))
    image_dir = temp_dir / 'images'
    image_dir.mkdir(parents=True, exist_ok=True)

    html_parts = []
    mermaid_counter = [0]

    # ── 1. Cover Page ────────────────────────────────────────────
    logo_img = ""
    if LOGO_PATH.exists():
        logo_img = (
            f'<div class="cover-logo">'
            f'<img src="file://{LOGO_PATH.resolve()}" alt="Sup Devinci Rennes" />'
            f'</div>'
        )

    html_parts.append(f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<style>{CSS_STYLES}</style>
</head>
<body>

<div class="cover-page">
    {logo_img}
    <div class="cover-line"></div>
    <h1 class="cover-title">Agentic Developer<br/>Craftsmanship</h1>
    <p class="cover-subtitle">Construisez des systèmes agentiques professionnels<br/>de l'histoire de l'IA au déploiement en production</p>
    <div class="cover-line" style="margin-top: 0;"></div>
    <div class="cover-meta">
        <strong>Auteur</strong> &mdash; Youghourta Merabtène<br/>
        <strong>Institution</strong> &mdash; Sup Devinci Rennes<br/>
        <strong>Version</strong> &mdash; {VERSION}
    </div>
    <div class="cover-version">v{VERSION}</div>
</div>
''')

    # ── 2. Table of Contents ──────────────────────────────────────
    html_parts.append('<div class="toc-page">')
    html_parts.append('<h1 class="toc-title">Table des matières</h1>')
    html_parts.append('<ul class="toc-list">')

    current_phase = None
    for fname, label, phase in CHAPTERS:
        if phase and phase != current_phase:
            current_phase = phase
            html_parts.append(f'<li class="toc-phase">{phase}</li>')
        html_parts.append(f'<li class="toc-item toc-chapter"><a href="#{slugify(label)}">{label}</a></li>')

    html_parts.append('<li class="toc-phase">Annexes</li>')
    for fname, label in APPENDICES:
        html_parts.append(f'<li class="toc-item toc-appendix"><a href="#{slugify(label)}">{label}</a></li>')

    html_parts.append('</ul></div>')

    # ── 3. Chapters ──────────────────────────────────────────────
    current_phase = None
    phase_num = 0

    for fname, label, phase in CHAPTERS:
        filepath = COURSE_DIR / fname
        if not filepath.exists():
            print(f"  WARNING: {filepath} not found, skipping")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Remove the first h1 if it exists (we use our own headers)
        md_content = re.sub(r'^#\s+.*$', '', md_content, count=1, flags=re.MULTILINE)

        # Render mermaid diagrams
        md_content = render_mermaid_blocks(md_content, temp_dir, image_dir, mermaid_counter)

        # Convert to HTML
        chapter_html = md_to_html(md_content)

        # Phase divider
        if phase and phase != current_phase:
            current_phase = phase
            phase_num += 1
            html_parts.append(f'''
<div class="phase-divider">
    <h1>Phase {phase_num}</h1>
    <div class="phase-line"></div>
    <p class="phase-desc">{phase}</p>
</div>
''')

        # Chapter
        title = extract_title(open(filepath, encoding='utf-8').read())
        if not title:
            title = label

        phase_attr = f'data-phase="{phase}"' if phase else ''
        html_parts.append(f'''
<div class="chapter-container" data-chapter="{label}" {phase_attr}>
    <div class="chapter-header">
        <h1>{title}</h1>
        <div class="chapter-meta">{phase if phase else ''}</div>
    </div>
    {chapter_html}
</div>
''')

    # ── 4. Appendices ──────────────────────────────────────────────
    html_parts.append('<div class="appendix-container">')

    for fname, label in APPENDICES:
        filepath = COURSE_DIR / fname
        if not filepath.exists():
            print(f"  WARNING: {filepath} not found, skipping")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if fname.endswith('.yml'):
            # Wrap YAML in code block
            md_content = f"```yaml\n{content}\n```"
        else:
            md_content = content

        appendix_html = md_to_html(md_content)

        html_parts.append(f'''
<div class="appendix-container">
    <div class="appendix-header">
        <h1>{label}</h1>
        <div class="appendix-meta">{fname}</div>
    </div>
    {appendix_html}
</div>
''')

    html_parts.append('</div>')
    html_parts.append('</body></html>')

    return '\n'.join(html_parts), temp_dir


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"Agentic Developer Craftsmanship — PDF Builder v{VERSION}")
    print("=" * 60)

    # Step 1: Build HTML
    print("\n[1/3] Construction du document HTML...")
    html_content, temp_dir = build_html()
    html_file = temp_dir / "document.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"  HTML généré : {html_file}")
    print(f"  Diagrammes dans : {temp_dir / 'images'}")

    # Step 2: Generate PDF
    print("\n[2/3] Génération du PDF avec WeasyPrint...")
    try:
        HTML(filename=str(html_file)).write_pdf(str(OUTPUT_PDF))
        print(f"  PDF généré : {OUTPUT_PDF}")
        print(f"  Taille : {OUTPUT_PDF.stat().st_size / 1024 / 1024:.1f} Mo")
    except Exception as e:
        print(f"  ERREUR : {e}")
        # Save HTML for debugging
        debug_html = COURSE_DIR / f"debug-v{VERSION}.html"
        shutil.copy(html_file, debug_html)
        print(f"  HTML de debug sauvegardé : {debug_html}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print(f"\n[3/3] Nettoyage terminé.")
    print(f"\n✅ PDF prêt : {OUTPUT_PDF}")

    # Summary
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print(f"  Document  : Agentic-Developer-Craftsmanship-v{VERSION}.pdf")
    print(f"  Chapitres : {len(CHAPTERS)}")
    print(f"  Annexes   : {len(APPENDICES)}")
    print(f"  Version   : {VERSION}")
    print(f"  Auteur    : Youghourta Merabtène")
    print(f"  Institution : Sup Devinci Rennes")
    print("=" * 60)


if __name__ == '__main__':
    main()
