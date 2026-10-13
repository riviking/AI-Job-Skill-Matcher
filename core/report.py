"""Generate a downloadable PDF report. Owner: Rivindu."""
from fpdf import FPDF


def _safe(text: str) -> str:
    return str(text).encode("latin-1", "replace").decode("latin-1")


def make_pdf(skills: list[str], results: list[dict]) -> bytes:
    """results: [{title, score, have, missing, courses:{skill:[{title,provider,url}]}}]"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "AI Job & Skill Matcher - Your Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, _safe("Your skills: " + ", ".join(skills)))
    for i, r in enumerate(results, 1):
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, _safe(f"{i}. {r['title']} - {r['score']:.0%} match"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, _safe("You have: " + (", ".join(r["have"]) or "-")))
        pdf.multi_cell(0, 6, _safe("Missing: " + (", ".join(r["missing"]) or "-")))
        for skill, courses in r["courses"].items():
            for c in courses:
                pdf.multi_cell(0, 6, _safe(f"  - {skill}: {c['title']} ({c['provider']}) {c['url']}"))
    return bytes(pdf.output())
