from flask import Flask, render_template, request, jsonify, send_file
import os
import datetime
import stripe
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
DOMAIN = os.environ.get('BASE_URL', 'http://localhost:5000')

LINKS = {
    "matcha": "https://amzn.to/3OqrkJE",
    "nmn": "https://www.iherb.com/c/nmn?rcode=YOUR_CODE",
    "spermidine": "https://www.iherb.com/c/spermidine?rcode=YOUR_CODE",
    "omega3": "https://www.iherb.com/c/omega-3-fish-oil?rcode=YOUR_CODE",
    "cooker": "https://amzn.to/3Oq6KZZ"
}

latest_score = 0

@app.route('/')
def index():
    return render_template('index.html', stripe_publishable_key=os.environ.get('STRIPE_PUBLISHABLE_KEY'))

@app.route('/api/calculate_score', methods=['POST'])
def calculate_score():
    data = request.json
    score = sum(1 for item in ['rice', 'miso_soup', 'seaweed', 'pickles', 'green_yellow_veg', 'fish', 'green_tea'] if data.get(item))
    if not data.get('beef_pork', False): score += 1
    global latest_score
    latest_score = score
    return jsonify({"score": score})

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': 'ZenGen Premium Report'}, 'unit_amount': 500}, 'quantity': 1}],
            mode='payment',
            locale='en',
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/',
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
def success(): return render_template('success.html')

@app.route('/download-report')
def download_report():
    global latest_score
    user_score = latest_score
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 1.0 * inch
    accent = colors.HexColor("#99ff00")

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.textColor, styleN.fontSize, styleN.leading = colors.white, 8, 10

    # --- PAGE 1: FULL BLUEPRINT ---
    c.setFillColorRGB(0.05, 0.05, 0.05)
    c.rect(0, 0, width, height, fill=True)
    
    # Header & ID
    c.setStrokeColor(accent)
    c.setLineWidth(2)
    c.line(margin, height - 1.2*inch, width - margin, height - 1.2*inch)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.white)
    c.drawString(margin, height - 1.0*inch, "OFFICIAL LONGEVITY BLUEPRINT")
    report_id = f"GEN-{datetime.datetime.now().strftime('%M%S')}"
    c.setFont("Helvetica", 8)
    c.drawRightString(width - margin, height - 1.0*inch, f"ID: {report_id} | {datetime.date.today()}")

    # Score Circle
    c.setStrokeColor(accent)
    c.circle(width/2, height - 2.4*inch, 0.6*inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 2.5*inch, f"{user_score}/8")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(accent)
    c.drawCentredString(width/2, height - 3.2*inch, "JDI8 SCORE")

    # Section 01: Bio-Marker Analysis
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, height - 3.6*inch, "01 // BIO-MARKER ANALYSIS")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.white)
    y = height - 3.85*inch
    analysis_points = [
        f"- Foundational Carbs: {'Optimal' if user_score > 5 else 'Sub-optimal'}.",
        f"- Seaweed Enzyme Activation: {'High' if user_score > 4 else 'Low'}.",
        "- Green Tea EGCG Intake: Critical for cellular repair."
    ]
    for line in analysis_points:
        c.drawString(margin + 0.2*inch, y, line)
        y -= 0.18*inch

    # Section 02: Genetic Edge (復活！)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(accent)
    c.drawString(margin, y - 0.1*inch, "02 // THE JAPANESE GENETIC EDGE")
    c.setFont("Helvetica-Oblique", 8.5)
    c.setFillColor(colors.white)
    c.drawString(margin + 0.2*inch, y - 0.3*inch, "Genetic Insight: Bacteroides plebeius")
    c.setFont("Helvetica", 8.5)
    c.drawString(margin + 0.2*inch, y - 0.5*inch, "Nature (2010) identifies your unique Porphyranase enzyme pathway.")
    y = y - 0.65*inch

    # Section 03: Protocol Table
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(accent)
    c.drawString(margin, y - 0.1*inch, "03 // 1-WEEK PROTOCOL")
    data = [
        ['Day', 'Focus', 'Action'],
        ['Mon', 'Autophagy', Paragraph('16:8 Fasting. Break with Miso.', styleN)],
        ['Tue', 'Microbiome', Paragraph('Natto/Okra. Feed the mucosa.', styleN)],
        ['Wed', 'Enzyme', Paragraph('Seaweed Salad. Activate Porphyranase.', styleN)],
        ['Thu', 'Recovery', Paragraph('2g Ippodo Matcha. L-Theanine spike.', styleN)],
        ['Fri', 'Omega-3', Paragraph('Fatty fish / EPA-DHA supplement.', styleN)],
        ['Sat', 'Metabolism', Paragraph('HIIT Session. Activate glycolysis.', styleN)],
        ['Sun', 'Rest', Paragraph('Hot Bath / Sauna. HSP activation.', styleN)]
    ]
    table = Table(data, colWidths=[0.7*inch, 1.1*inch, 4.4*inch], rowHeights=0.4*inch)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, margin, y - 0.4*inch - (0.4*inch * 8))

    c.showPage() # --- PAGE 2 ---
    c.setFillColorRGB(0.05, 0.05, 0.05)
    c.rect(0, 0, width, height, fill=True)
    c.setStrokeColor(accent)
    c.line(margin, height - 1.2*inch, width - margin, height - 1.2*inch)
    
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(accent)
    c.drawString(margin, height - 1.8*inch, "04 // THE GOLD STANDARD STACK")
    
    y = height - 2.3*inch
    stack = [
        ("Ippodo Matcha", LINKS['matcha'], "Finest L-Theanine for neuro-protection."),
        ("Suntory NMN", LINKS['nmn'], "99.9% purity for DNA cellular repair."),
        ("Spermidine", LINKS['spermidine'], "Autophagy inducer for cellular health."),
        ("EPA / DHA", LINKS['omega3'], "1-2g daily for inflammation control."),
        ("Zojirushi IH", LINKS['cooker'], "Metabolism foundation. GABA mode.")
    ]
    for title, link, desc in stack:
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.white)
        c.drawString(margin, y, f"> {title}:")
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.lightgrey)
        c.drawString(margin + 1.6*inch, y, desc)
        c.linkURL(link, (margin, y-5, margin+450, y+15), relative=1)
        y -= 0.45*inch

    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.grey)
    c.drawCentredString(width/2, 0.5*inch, "Based on Japanese Diet Index (JDI8) research. Not medical advice.")

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='ZENGEN_Premium_Report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))