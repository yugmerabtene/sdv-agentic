"""Generate a one-page Syllabus PDF with logo and table of contents."""

import sys
import base64
from datetime import datetime
sys.path.insert(0, '/home/yug/Documents/Agentic-Developer-Craftsmanship')

from build_site import build_toc_html, VERSION
from weasyprint import HTML as WeasyHTML

FR_MONTHS = {1:"janvier",2:"février",3:"mars",4:"avril",5:"mai",6:"juin",7:"juillet",8:"août",9:"septembre",10:"octobre",11:"novembre",12:"décembre"}
TODAY = datetime.now()
TODAY_STR = f"{TODAY.day} {FR_MONTHS[TODAY.month]} {TODAY.year}"

OUTPUT_PDF = '/home/yug/Documents/Agentic-Developer-Craftsmanship/export/pdf/syllabus.pdf'
LOGO_PATH = '/home/yug/Documents/Agentic-Developer-Craftsmanship/export/site/img/logo.jpeg'

# Embed logo as base64 for reliable PDF rendering
with open(LOGO_PATH, 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()
LOGO_DATA_URI = f'data:image/jpeg;base64,{logo_b64}'

toc_html = build_toc_html(include_prerequis=True)

html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Syllabus — Agentic Developer Craftsmanship v{VERSION}</title>
<style>
@page {{
    size: A4;
    margin: 1.5cm 1.5cm 1.5cm 1.5cm;
    @bottom-center {{
        content: "Agentic Developer Craftsmanship v" "{VERSION}" " — Auteur : Youghourta Merabtène — https://yug.be — yug.merabtene@gmail.com — Sup Devinci Rennes";
        font-size: 7.5pt;
        color: #94a3b8;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}
}}
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}
body {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 8.5pt;
    color: #1e293b;
    line-height: 1.35;
}}
.logo-header {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 0.4cm;
}}
.logo-header img {{
    height: 52px;
    width: auto;
}}
.title-block {{
    text-align: right;
}}
.title-block h1 {{
    font-size: 17pt;
    color: #0f172a;
    font-weight: 700;
    letter-spacing: -0.3pt;
    margin: 0;
    line-height: 1.1;
}}
.title-block .subtitle {{
    font-size: 9pt;
    color: #64748b;
    margin-top: 2px;
}}
.title-block .date {{
    font-size: 9pt;
    color: #64748b;
    margin-top: 1px;
}}
.divider {{
    height: 1.5px;
    background: linear-gradient(90deg, #1e3a5f, #2563eb, #7c3aed);
    margin-bottom: 0.35cm;
    border: none;
}}
.toc-list {{
    list-style: none;
    padding: 0;
    column-count: 2;
    column-gap: 1cm;
    column-rule: 0.5px solid #e2e8f0;
}}
.toc-list li {{
    break-inside: avoid;
    padding: 0;
    margin: 0;
}}
.toc-chapter {{
    list-style: none;
}}
.toc-chapter a {{
    display: block;
    font-size: 9pt;
    font-weight: 600;
    color: #0f172a;
    text-decoration: none;
    padding: 1.5px 0 1px 5px;
    border-left: 2px solid #1e3a5f;
    margin-top: 2px;
    line-height: 1.25;
}}
.toc-chapter a.annexe {{
    border-left-color: #7c3aed;
    margin-top: 4px;
}}
.toc-sub {{
    list-style: none;
}}
.opensource-note {{
    text-align: center;
    font-size: 7.5pt;
    color: #64748b;
    margin-top: 0.5cm;
    padding-top: 0.3cm;
    border-top: 1px solid #e2e8f0;
}}
.repo-link {{
    text-align: center;
    font-size: 7.5pt;
    color: #64748b;
    margin-top: 0.2cm;
    line-height: 1.4;
}}

.toc-sub a {{
    display: block;
    font-size: 8pt;
    color: #475569;
    text-decoration: none;
    padding: 0.3px 0 0.3px 12px;
    line-height: 1.2;
}}
</style>
</head>
<body>

<div class="logo-header">
    <img src="{LOGO_DATA_URI}" alt="Sup Devinci Rennes">
    <div class="title-block">
        <h1>Syllabus</h1>
        <div class="subtitle">Agentic Developer Craftsmanship &mdash; v{VERSION}</div>
        <div class="date">{TODAY_STR}</div>
    </div>
</div>

<div class="divider"></div>

<ul class="toc-list">
    {toc_html}
</ul>

<div class="opensource-note">Ce cours utilise exclusivement des technologies <strong>open-source</strong> et <strong>gratuites</strong> — aucun abonnement API payant requis.</div>

<div class="repo-link">L'intégralité du cours et des labs est disponible sur GitHub&nbsp;:<br/><strong>https://github.com/yugmerabtene/Agentic-Developer-Craftsmanship</strong></div>

</body>
</html>
'''

print("Génération du PDF Syllabus...")
WeasyHTML(string=html_content).write_pdf(OUTPUT_PDF)
print(f"  syllabus.pdf généré : {OUTPUT_PDF}")
