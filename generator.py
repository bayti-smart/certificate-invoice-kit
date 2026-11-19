"""Free PDF certificate and invoice generator.

Usage:
  python generator.py certificate --name "Jane Doe" --course "Python Basics" --out cert.pdf
  python generator.py invoice --client "Acme Ltd" --items "Design work:1:250" "Hosting:12:5" --out inv.pdf
Items are written as description:quantity:unit_price
"""
import argparse
from datetime import date
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

NAVY = colors.HexColor("#1f2a44")
GOLD = colors.HexColor("#b8923a")
GREY = colors.HexColor("#6b7280")


def certificate(name, course, issuer, out, when=None):
    when = when or date.today().strftime("%B %d, %Y")
    w, h = landscape(A4)
    c = canvas.Canvas(out, pagesize=(w, h))
    c.setStrokeColor(NAVY); c.setLineWidth(6); c.rect(12*mm, 12*mm, w-24*mm, h-24*mm)
    c.setStrokeColor(GOLD); c.setLineWidth(1.5); c.rect(18*mm, 18*mm, w-36*mm, h-36*mm)
    c.setFillColor(NAVY); c.setFont("Times-Bold", 42)
    c.drawCentredString(w/2, h-60*mm, "CERTIFICATE")
    c.setFillColor(GOLD); c.setFont("Times-Roman", 18)
    c.drawCentredString(w/2, h-72*mm, "OF ACHIEVEMENT")
    c.setFillColor(GREY); c.setFont("Helvetica", 13)
    c.drawCentredString(w/2, h-95*mm, "This certificate is proudly presented to")
    c.setFillColor(NAVY); c.setFont("Times-BoldItalic", 38)
    c.drawCentredString(w/2, h-115*mm, name)
    c.setStrokeColor(GOLD); c.setLineWidth(1)
    c.line(w/2-70*mm, h-120*mm, w/2+70*mm, h-120*mm)
    c.setFillColor(GREY); c.setFont("Helvetica", 13)
    c.drawCentredString(w/2, h-135*mm, "for successfully completing")
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w/2, h-148*mm, course)
    c.setFillColor(GREY); c.setFont("Helvetica", 11)
    c.line(40*mm, 38*mm, 100*mm, 38*mm); c.drawCentredString(70*mm, 32*mm, "Date: " + when)
    c.line(w-100*mm, 38*mm, w-40*mm, 38*mm); c.drawCentredString(w-70*mm, 32*mm, issuer)
    c.save()


def invoice(client, items, out, seller="Your Business", number=None, tax=0.0):
    w, h = A4
    number = number or date.today().strftime("INV-%Y%m%d-001")
    c = canvas.Canvas(out, pagesize=A4)
    c.setFillColor(NAVY); c.rect(0, h-38*mm, w, 38*mm, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 26)
    c.drawString(20*mm, h-24*mm, "INVOICE")
    c.setFont("Helvetica", 11); c.drawRightString(w-20*mm, h-20*mm, seller)
    c.drawRightString(w-20*mm, h-27*mm, number)
    c.setFillColor(GREY); c.setFont("Helvetica", 10)
    c.drawString(20*mm, h-52*mm, "BILL TO"); c.drawRightString(w-20*mm, h-52*mm, "DATE")
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 13)
    c.drawString(20*mm, h-59*mm, client)
    c.drawRightString(w-20*mm, h-59*mm, date.today().strftime("%B %d, %Y"))
    rows = [["Description", "Qty", "Unit price", "Amount"]]
    subtotal = 0.0
    for d, q, p in items:
        amt = q*p; subtotal += amt
        rows.append([d, f"{q:g}", f"{p:,.2f}", f"{amt:,.2f}"])
    t = Table(rows, colWidths=[90*mm, 20*mm, 30*mm, 30*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    tw, th = t.wrapOn(c, w, h); t.drawOn(c, 20*mm, h-72*mm-th)
    y = h-72*mm-th-12*mm
    tax_amt = subtotal*tax
    c.setFont("Helvetica", 11); c.setFillColor(GREY)
    c.drawRightString(w-50*mm, y, "Subtotal"); c.drawRightString(w-20*mm, y, f"{subtotal:,.2f}")
    if tax:
        y -= 7*mm; c.drawRightString(w-50*mm, y, f"Tax ({tax:.0%})"); c.drawRightString(w-20*mm, y, f"{tax_amt:,.2f}")
    y -= 9*mm; c.setFont("Helvetica-Bold", 14); c.setFillColor(NAVY)
    c.drawRightString(w-50*mm, y, "TOTAL"); c.drawRightString(w-20*mm, y, f"{subtotal+tax_amt:,.2f}")
    c.setFont("Helvetica", 9); c.setFillColor(GREY)
    c.drawCentredString(w/2, 15*mm, "Thank you for your business.")
    c.save()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("certificate")
    a.add_argument("--name", required=True); a.add_argument("--course", required=True)
    a.add_argument("--issuer", default="Director"); a.add_argument("--out", default="certificate.pdf")
    b = s.add_parser("invoice")
    b.add_argument("--client", required=True); b.add_argument("--items", nargs="+", required=True)
    b.add_argument("--seller", default="Your Business"); b.add_argument("--tax", type=float, default=0.0)
    b.add_argument("--out", default="invoice.pdf")
    r = p.parse_args()
    if r.cmd == "certificate":
        certificate(r.name, r.course, r.issuer, r.out)
    else:
        items = [(d, float(q), float(u)) for d, q, u in (i.rsplit(":", 2) for i in r.items)]
        invoice(r.client, items, r.out, r.seller, tax=r.tax)
    print("Saved", r.out)


if __name__ == "__main__":
    main()
