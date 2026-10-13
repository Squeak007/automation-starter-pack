"""invoice_pdf.py — Generate a clean one-page PDF invoice from a JSON spec.

Usage:
    python invoice_pdf.py example_invoice.json

Spec format:
{
  "from":   {"name": "Squeak Co.", "email": "...", "address": "..."},
  "to":     {"name": "Client Co.", "email": "...", "address": "..."},
  "number": "SQ-001",
  "date":   "2026-10-13",
  "due":    "2026-10-27",
  "items":  [{"desc": "Blog post", "qty": 1, "rate": 150.00}, ...],
  "notes":  "Thanks for your business."
}
"""

import argparse
import json
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def build(spec: dict, out_path: str) -> None:
    doc = SimpleDocTemplate(out_path, pagesize=LETTER, topMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("INVOICE", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))

    header = [
        ["From:", spec["from"]["name"], "Invoice #:", spec["number"]],
        ["", spec["from"].get("email", ""), "Date:", spec["date"]],
        ["", spec["from"].get("address", ""), "Due:", spec["due"]],
        ["", "", "", ""],
        ["Bill to:", spec["to"]["name"], "", ""],
        ["", spec["to"].get("email", ""), "", ""],
        ["", spec["to"].get("address", ""), "", ""],
    ]
    t = Table(header, colWidths=[0.8 * inch, 3.2 * inch, 1.0 * inch, 1.5 * inch])
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "Helvetica"), ("FONTSIZE", (0, 0), (-1, -1), 10)]))
    story.append(t)
    story.append(Spacer(1, 0.3 * inch))

    rows = [["Description", "Qty", "Rate", "Amount"]]
    total = 0.0
    for item in spec["items"]:
        amount = item["qty"] * item["rate"]
        total += amount
        rows.append([item["desc"], str(item["qty"]), f"${item['rate']:.2f}", f"${amount:.2f}"])
    rows.append(["", "", "Total:", f"${total:.2f}"])

    table = Table(rows, colWidths=[3.5 * inch, 0.8 * inch, 1.0 * inch, 1.2 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -2), 0.25, colors.grey),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
    ]))
    story.append(table)

    if spec.get("notes"):
        story.append(Spacer(1, 0.4 * inch))
        story.append(Paragraph(f"<i>{spec['notes']}</i>", styles["Normal"]))

    doc.build(story)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", help="Path to a JSON invoice spec")
    parser.add_argument("--out", help="Output PDF path (default: invoice-<number>.pdf)")
    args = parser.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    out = args.out or f"invoice-{spec['number']}.pdf"
    build(spec, out)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
