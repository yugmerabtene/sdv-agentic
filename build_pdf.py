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
from build_site import build_prerequisites_html

# ─── Configuration ───────────────────────────────────────────────────────────

COURSE_DIR = Path("/home/yug/Documents/Agentic-Developer-Craftsmanship")
VERSION = "1.3"
OUTPUT_PDF = COURSE_DIR / f"Agentic-Developer-Craftsmanship-v{VERSION}.pdf"
LOGO_PATH = COURSE_DIR / "logo.jpeg"

CHAPTERS = [
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

PHASES = [
    ("Phase 1", "Fondamentaux", "De l'histoire de l'IA aux bases des LLM", "#1e3a5f"),
    ("Phase 2", "Interaction avec les LLMs", "Prompt engineering, tool use et boucle agent", "#2563eb"),
    ("Phase 3", "Mémoire & Collaboration", "RAG, mémoire persistante et systèmes multi-agents", "#059669"),
    ("Phase 4", "Production", "MCP, CI/CD et déploiement professionnel", "#7c3aed"),
    ("Phase 5", "Mise en pratique", "Sécurité et labs opencode complets", "#d97706"),
]

LOGO_BASE64 = None
if LOGO_PATH.exists():
    import base64
    with open(LOGO_PATH, 'rb') as f:
        LOGO_BASE64 = base64.b64encode(f.read()).decode()

LOGO_DATA_URI = f"data:image/jpeg;base64,{LOGO_BASE64}" if LOGO_BASE64 else ""

# ─── CSS Stylesheet ──────────────────────────────────────────────────────────

CSS_STYLES = f"""
@page {{
    size: A4;
    margin: 2.8cm 2.5cm 3cm 2.5cm;

    @top-left {{
        content: string(title);
        font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
        font-size: 7.5pt;
        color: #475569;
        margin-top: 2pt;
    }}

    @top-right {{
        content: string(chapter);
        font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
        font-size: 7.5pt;
        color: #94a3b8;
        margin-top: 2pt;
    }}

    @bottom-center {{
        content: "—  " counter(page) "  —";
        font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
    }}
}}

@page cover {{
    margin: 0;
    @top-left {{ content: none; }}
    @top-right {{ content: none; }}
    @bottom-center {{ content: none; }}
}}

@page toc {{
    @top-left {{ content: none; }}
    @top-right {{ content: none; }}
}}

@page chapter-first {{
    @top-left {{ content: none; }}
    @top-right {{ content: none; }}
}}

* {{ box-sizing: border-box; }}

html {{
    font-family: 'DejaVu Serif', 'Liberation Serif', serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1e293b;
}}

body {{
    margin: 0;
    padding: 0;
    string-set: title "Agentic Developer Craftsmanship";
}}

/* ─── Cover Page ───────────────────────────────────────────────────── */

.cover-page {{
    page: cover;
    break-after: page;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: linear-gradient(160deg, #0f172a 0%, #1e3a5f 40%, #1e40af 70%, #0f172a 100%);
    color: #ffffff;
    text-align: center;
    padding: 4cm;
    position: relative;
    overflow: hidden;
}}

.cover-page::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
        radial-gradient(ellipse at 20% 20%, rgba(59, 130, 246, 0.2) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(37, 99, 235, 0.08) 0%, transparent 70%);
}}

.cover-logo {{
    margin-bottom: 2.5cm;
    position: relative;
    z-index: 1;
}}
.cover-logo img {{
    width: 110px;
    height: 110px;
    border-radius: 50%;
    border: 3px solid rgba(255,255,255,0.25);
    padding: 5px;
    box-shadow: 0 0 40px rgba(59, 130, 246, 0.3);
}}

.cover-line {{
    width: 100px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #60a5fa, transparent);
    margin: 1.2cm auto;
    position: relative;
    z-index: 1;
}}

.cover-title {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 28pt;
    font-weight: 700;
    letter-spacing: -0.5px;
    line-height: 1.15;
    margin: 0 0 0.4cm 0;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}}

.cover-subtitle {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 13pt;
    font-weight: 300;
    color: #93c5fd;
    margin: 0 0 1.5cm 0;
    position: relative;
    z-index: 1;
    line-height: 1.5;
}}

.cover-meta {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 10pt;
    color: #94a3b8;
    margin-top: auto;
    position: relative;
    z-index: 1;
    line-height: 2;
}}
.cover-meta strong {{
    color: #e2e8f0;
    font-weight: 600;
}}

.cover-version {{
    position: absolute;
    bottom: 1.8cm;
    right: 3cm;
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 8pt;
    color: #64748b;
    background: rgba(15, 23, 42, 0.6);
    padding: 3px 14px;
    border-radius: 12px;
    border: 1px solid rgba(148, 163, 184, 0.15);
    z-index: 1;
}}

/* ─── Table of Contents ────────────────────────────────────────────── */

.toc-page {{
    page: toc;
    break-after: page;
    padding: 0 0.5cm;
}}

.toc-header {{
    background: linear-gradient(135deg, #1e3a5f, #2563eb);
    color: #ffffff;
    padding: 1cm 1.5cm;
    margin: 0 -0.5cm 0.8cm -0.5cm;
}}

.toc-header h1 {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 20pt;
    font-weight: 700;
    margin: 0;
    color: #ffffff;
}}

.toc-header p {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    color: #93c5fd;
    margin: 4pt 0 0 0;
}}

.toc-list {{
    list-style: none;
    padding: 0;
    margin: 0;
}}

.toc-phase-li {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 700;
    color: #1e3a5f;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 12pt 0 4pt 0;
    border-bottom: 2px solid #1e3a5f;
    margin-top: 6pt;
}}

.toc-item {{
    padding: 5pt 0 5pt 14pt;
    border-bottom: 1px dotted #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}}

.toc-item a {{
    color: #1e293b;
    text-decoration: none;
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 10pt;
    flex: 1;
    padding-right: 10pt;
}}

.toc-item a::after {{
    content: target-counter(attr(href), page);
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    color: #2563eb;
    font-weight: 600;
    float: right;
}}

.toc-item a:hover {{
    color: #2563eb;
}}

.toc-chapter {{
    font-weight: 500;
}}

.toc-preference {{
    font-style: italic;
    color: #64748b;
}}

.toc-appendix-li {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 700;
    color: #7c3aed;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 12pt 0 4pt 0;
    border-bottom: 2px solid #7c3aed;
    margin-top: 10pt;
}}

.toc-appendix-item {{
    padding: 5pt 0 5pt 14pt;
    border-bottom: 1px dotted #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}}

.toc-appendix-item a {{
    color: #1e293b;
    text-decoration: none;
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 10pt;
    flex: 1;
    padding-right: 10pt;
}}

.toc-appendix-item a::after {{
    content: target-counter(attr(href), page);
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    color: #7c3aed;
    font-weight: 600;
    float: right;
}}

/* ─── Phase divider ────────────────────────────────────────────────── */

.phase-divider {{
    page: chapter-first;
    page-break-before: always;
    break-before: page;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    text-align: center;
    padding: 2cm;
    position: relative;
    overflow: hidden;
}}

.phase-divider::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
        radial-gradient(ellipse at 50% 30%, rgba(37, 99, 235, 0.06) 0%, transparent 60%);
}}

.phase-divider .phase-num {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 48pt;
    font-weight: 900;
    color: #1e3a5f;
    opacity: 0.15;
    position: absolute;
    top: 1cm;
    right: 1.5cm;
    line-height: 1;
}}

.phase-divider .phase-badge {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 9pt;
    font-weight: 700;
    color: #ffffff;
    background: linear-gradient(135deg, #1e3a5f, #2563eb);
    padding: 4pt 16pt;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.6cm;
    position: relative;
}}

.phase-divider h1 {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 24pt;
    font-weight: 700;
    color: #1e3a5f;
    margin: 0 0 0.3cm 0;
    position: relative;
}}

.phase-divider .phase-line {{
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #2563eb, transparent);
    margin: 0.5cm auto;
    position: relative;
}}

.phase-divider .phase-desc {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 11pt;
    color: #64748b;
    max-width: 70%;
    margin: 0 auto;
    position: relative;
    line-height: 1.5;
}}

/* ─── Prerequis section ────────────────────────────────────────────── */

.prerequis-section {{
    padding-top: 0.6cm;
}}
.prerequis-section h2 {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 14pt;
    font-weight: 700;
    color: #1e3a5f;
    border-bottom: 2px solid #bfdbfe;
    padding-bottom: 4pt;
    margin: 0 0 0.3cm 0;
}}

/* ─── Chapter Styles ───────────────────────────────────────────────── */

.chapter-container {{
    page-break-before: always;
    string-set: chapter attr(data-chapter);
    break-before: page;
}}

.chapter-header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #2563eb 100%);
    color: #ffffff;
    padding: 1.5cm 2cm 0.8cm 2cm;
    margin: -0.3cm -0.3cm 0.8cm -0.3cm;
    position: relative;
    overflow: hidden;
}}

.chapter-header::before {{
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
}}

.chapter-header h1 {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 18pt;
    font-weight: 700;
    margin: 0;
    line-height: 1.3;
    color: #ffffff;
    position: relative;
}}

.chapter-header .chapter-meta {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 8.5pt;
    color: #93c5fd;
    margin-top: 6pt;
    letter-spacing: 0.3px;
    position: relative;
}}

/* ─── Appendix styles ──────────────────────────────────────────────── */

.appendix-container {{
    page-break-before: always;
    string-set: chapter "Annexes";
    break-before: page;
}}

.appendix-header {{
    background: linear-gradient(135deg, #0f172a, #4c1d95);
    color: #ffffff;
    padding: 1.2cm 1.5cm 0.6cm 1.5cm;
    margin: -0.3cm -0.3cm 0.8cm -0.3cm;
    position: relative;
}}

.appendix-header h1 {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 16pt;
    font-weight: 700;
    margin: 0;
    color: #ffffff;
}}

.appendix-header .appendix-meta {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    font-size: 8pt;
    color: #a78bfa;
    margin-top: 4pt;
}}

/* ─── Typography ───────────────────────────────────────────────────── */

h1, h2, h3, h4, h5, h6 {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    color: #1e3a5f;
    margin: 0.6cm 0 0.3cm 0;
    line-height: 1.3;
}}

h2 {{
    font-size: 14pt;
    border-bottom: 2px solid #bfdbfe;
    padding-bottom: 4pt;
    color: #1e40af;
}}

h3 {{
    font-size: 12pt;
    color: #2563eb;
}}

h4 {{ font-size: 11pt; }}
h5 {{ font-size: 10.5pt; }}
h6 {{ font-size: 10pt; color: #64748b; }}

p {{ margin: 0 0 0.35cm 0; text-align: justify; }}

a {{ color: #2563eb; text-decoration: none; }}

strong {{ color: #0f172a; }}
em {{ font-style: italic; }}

/* ─── Code Blocks ──────────────────────────────────────────────────── */

pre {{
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #2563eb;
    border-radius: 4px;
    padding: 10pt 12pt;
    font-family: 'DejaVu Sans Mono', 'Liberation Mono', monospace;
    font-size: 8pt;
    line-height: 1.45;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
    margin: 0.35cm 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

code {{
    font-family: 'DejaVu Sans Mono', 'Liberation Mono', monospace;
    font-size: 8.5pt;
    background: #eef2ff;
    padding: 1pt 4pt;
    border-radius: 3px;
    color: #1e40af;
}}

pre code {{
    background: none;
    padding: 0;
    font-size: inherit;
    color: #1e293b;
}}

/* ─── Tables ───────────────────────────────────────────────────────── */

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0.4cm 0;
    font-size: 9pt;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

th {{
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    background: #1e3a5f;
    color: #ffffff;
    padding: 6pt 8pt;
    text-align: left;
    font-weight: 600;
    font-size: 8.5pt;
    letter-spacing: 0.3px;
}}

td {{
    padding: 5pt 8pt;
    border-bottom: 1px solid #e2e8f0;
}}

tr:nth-child(even) td {{
    background: #f8fafc;
}}

/* ─── Blockquotes / Admonitions ────────────────────────────────────── */

blockquote {{
    margin: 0.4cm 0;
    padding: 8pt 14pt;
    border-left: 4px solid #2563eb;
    background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
    border-radius: 0 4px 4px 0;
}}

blockquote p {{ margin: 0; }}

/* ─── Horizontal Rules ─────────────────────────────────────────────── */

hr {{
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 0.6cm 0;
}}

/* ─── Lists ────────────────────────────────────────────────────────── */

ul, ol {{
    margin: 0.2cm 0;
    padding-left: 1.2cm;
}}

li {{ margin-bottom: 3pt; }}

/* ─── Images ───────────────────────────────────────────────────────── */

img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0.4cm auto;
}}
"""


# ─── Helpers ─────────────────────────────────────────────────────────────────

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def extract_mermaid_blocks(md_content):
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
    m = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    return m.group(1).strip() if m else ""


# ─── Mermaid Rendering ───────────────────────────────────────────────────────

def render_mermaid_blocks(md_content, output_dir, image_dir, counter=[0]):
    blocks = extract_mermaid_blocks(md_content)
    if not blocks:
        return md_content

    result = md_content
    for block in reversed(blocks):
        counter[0] += 1
        seq = counter[0]
        mmd_file = output_dir / f"diagram-{seq:03d}.mmd"
        png_file = image_dir / f"diagram-{seq:03d}.png"

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

        rel_path = png_file.resolve()
        img_tag = f'\n\n![Diagramme {seq}]({rel_path})\n\n'
        before = result[:block['start']]
        after = result[block['end']:]
        result = before + img_tag + after

    return result


# ─── Markdown → HTML conversion ─────────────────────────────────────────────

def md_to_html(md_text, extensions=None):
    if extensions is None:
        extensions = [
            'extra',
            'codehilite',
            'toc',
            'smarty',
            'nl2br',
        ]
    return markdown.markdown(md_text, extensions=extensions)


# ─── Build combined HTML ─────────────────────────────────────────────────────

def build_html():
    temp_dir = Path(tempfile.mkdtemp(prefix='pdf_build_'))
    image_dir = temp_dir / 'images'
    image_dir.mkdir(parents=True, exist_ok=True)

    html_parts = []
    mermaid_counter = [0]

    logo_img_cover = ""
    if LOGO_PATH.exists():
        logo_img_cover = (
            f'<div class="cover-logo">'
            f'<img src="file://{LOGO_PATH.resolve()}" alt="Sup Devinci Rennes" />'
            f'</div>'
        )

    # ── 1. Cover Page ────────────────────────────────────────────────
    html_parts.append(f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<style>{CSS_STYLES}</style>
</head>
<body>

<div class="cover-page">
    {logo_img_cover}
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

    # ── 2. Table of Contents ──────────────────────────────────────────
    html_parts.append('<div class="toc-page">')
    html_parts.append('''<div class="toc-header">
        <h1>Table des matières</h1>
        <p>Agentic Developer Craftsmanship &mdash; v''' + VERSION + '''</p>
    </div>''')
    html_parts.append('<ul class="toc-list">')

    current_phase_name = None
    for fname, label, phase in CHAPTERS:
        if phase and phase != current_phase_name:
            current_phase_name = phase
            html_parts.append(f'<li class="toc-phase-li">{phase}</li>')
        chap_id = slugify(label)
        cls = 'toc-preference' if label == 'Préface' else 'toc-chapter'
        html_parts.append(
            f'<li class="toc-item {cls}"><a href="#{chap_id}">{label}</a></li>'
        )

    html_parts.append('<li class="toc-appendix-li">Annexes</li>')
    for fname, label in APPENDICES:
        app_id = slugify(label)
        html_parts.append(
            f'<li class="toc-appendix-item"><a href="#{app_id}">{label}</a></li>'
        )

    html_parts.append('</ul></div>')

    # ── 3. Chapters ──────────────────────────────────────────────────
    current_phase = None
    phase_num = 0
    chapter_count = 0

    for fname, label, phase in CHAPTERS:
        filepath = COURSE_DIR / fname
        if not filepath.exists():
            print(f"  WARNING: {filepath} not found, skipping")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()

        md_content = re.sub(r'^#\s+.*$', '', md_content, count=1, flags=re.MULTILINE)

        # Ch1 : split théorie / TP, insérer prerequis README entre les deux
        if chapter_count == 0:
            tp_marker = "## 6. Travaux Pratiques"
            tp_pos = md_content.find(tp_marker)
            if tp_pos != -1:
                ch1_theory = md_content[:tp_pos]
                ch1_tp = md_content[tp_pos:]

                ch1_theory = re.sub(
                    r'^## Prérequis\n.*?(?=\n## |\Z)',
                    '',
                    ch1_theory,
                    count=1,
                    flags=re.DOTALL | re.MULTILINE
                )

                ch1_theory = render_mermaid_blocks(ch1_theory, temp_dir, image_dir, mermaid_counter)
                ch1_tp = render_mermaid_blocks(ch1_tp, temp_dir, image_dir, mermaid_counter)

                prerequis_html = build_prerequisites_html()

                theory_html = md_to_html(ch1_theory)
                tp_html = md_to_html(ch1_tp)

                combined = theory_html
                if prerequis_html:
                    combined += f'<div class="prerequis-section" style="page-break-before: always;"><h2>Mise en place des prérequis</h2>{prerequis_html}</div>'
                combined += tp_html
                chapter_html = combined
            else:
                md_content = render_mermaid_blocks(md_content, temp_dir, image_dir, mermaid_counter)
                chapter_html = md_to_html(md_content)
        else:
            md_content = render_mermaid_blocks(md_content, temp_dir, image_dir, mermaid_counter)
            chapter_html = md_to_html(md_content)

        # Phase divider
        if phase and phase != current_phase:
            current_phase = phase
            phase_num += 1
            phase_title = PHASES[phase_num - 1][1] if phase_num <= len(PHASES) else phase
            phase_desc = PHASES[phase_num - 1][2] if phase_num <= len(PHASES) else ""
            html_parts.append(f'''
<div class="phase-divider">
    <div class="phase-num">0{phase_num}</div>
    <div class="phase-badge">Phase {phase_num}</div>
    <h1>{phase_title}</h1>
    <div class="phase-line"></div>
    <p class="phase-desc">{phase_desc}</p>
</div>
''')

        title = extract_title(open(filepath, encoding='utf-8').read())
        if not title:
            title = label

        chap_id = slugify(label)

        html_parts.append(f'''
<div class="chapter-container" id="{chap_id}" data-chapter="{label}">
    <div class="chapter-header">
        <h1>{title}</h1>
        <div class="chapter-meta">{phase if phase else ''}</div>
    </div>
    {chapter_html}
</div>
''')

        chapter_count += 1

    # ── 4. Appendices ────────────────────────────────────────────────
    for fname, label in APPENDICES:
        filepath = COURSE_DIR / fname
        if not filepath.exists():
            print(f"  WARNING: {filepath} not found, skipping")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if fname.endswith('.yml'):
            md_content = f"```yaml\n{content}\n```"
        else:
            md_content = content

        appendix_html = md_to_html(md_content)
        app_id = slugify(label)

        html_parts.append(f'''
<div class="appendix-container" id="{app_id}">
    <div class="appendix-header">
        <h1>{label}</h1>
        <div class="appendix-meta">{fname}</div>
    </div>
    {appendix_html}
</div>
''')

    html_parts.append('</body></html>')
    return '\n'.join(html_parts), temp_dir


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"Agentic Developer Craftsmanship — PDF Builder v{VERSION}")
    print("=" * 60)

    print("\n[1/3] Construction du document HTML...")
    html_content, temp_dir = build_html()
    html_file = temp_dir / "document.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"  HTML généré : {html_file}")
    print(f"  Diagrammes dans : {temp_dir / 'images'}")

    print("\n[2/3] Génération du PDF avec WeasyPrint...")
    try:
        HTML(filename=str(html_file)).write_pdf(str(OUTPUT_PDF))
        print(f"  PDF généré : {OUTPUT_PDF}")
        print(f"  Taille : {OUTPUT_PDF.stat().st_size / 1024 / 1024:.1f} Mo")
    except Exception as e:
        print(f"  ERREUR : {e}")
        import traceback
        traceback.print_exc()
        debug_html = COURSE_DIR / f"debug-v{VERSION}.html"
        shutil.copy(html_file, debug_html)
        print(f"  HTML de debug sauvegardé : {debug_html}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print(f"\n[3/3] Nettoyage terminé.")
    print(f"\n✅ PDF prêt : {OUTPUT_PDF}")

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
