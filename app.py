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
DOMAIN = os.environ.get('BASE_URL', 'https://zengen-longevity.onrender.com')

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

    # --- PAGE 1: PREMIUM DESIGN ---
    c.setFillColorRGB(0.05, 0.05, 0.05)
    c.rect(0, 0, width, height, fill=True)
    c.setStrokeColor(accent)
    c.setLineWidth(2)
    c.line(margin, height - 1.2*inch, width - margin, height - 1.2*inch)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.white)
    c.drawString(margin, height - 1.0*inch, "OFFICIAL LONGEVITY BLUEPRINT")

    # Score Circle
    c.setStrokeColor(accent)
    c.circle(width/2, height - 2.3*inch, 0.55*inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width/2, height - 2.4*inch, f"{user_score}/8")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(accent)
    c.drawCentredString(width/2, height - 3.0*inch, "JDI8 SCORE")

    # RISK ASSESSMENT (スコアの下に配置)
    risk = "LOW" if user_score > 6 else "MODERATE" if user_score > 3 else "HIGH"
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.white)
    c.drawCentredString(width/2, height - 3.3*inch, f"RISK ASSESSMENT: {risk}")

    # 02 Genetic Edge (復活)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(accent)
    c.drawString(margin, height - 3.7*inch, "02 // THE JAPANESE GENETIC EDGE")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.white)
    c.drawString(margin + 0.2*inch, height - 3.9*inch, "Nature (2010): Porphyranase enzyme pathway identified for marine processing.")

    # 全曜日のパーソナライズロジック
    if user_score <= 3: # 初級
        p_mon = "Hydration focus. Start with Miso soup to reset."
        p_tue = "Eat Natto at dinner to support mucosa."
        p_wed = "Add a small Seaweed side to your lunch."
        p_fri = "Omega-3: Take 1g EPA/DHA supplement."
        p_sun = "Focus on 20min hot soak to activate HSP."
    elif user_score <= 6: # 中級
        p_mon = "16:8 Fasting. Break fast with Miso & Seaweed."
        p_tue = "Microbiome Diversity: Mix Natto with Okra/Kimchi."
        p_wed = "Seaweed Salad. Activate Porphyranase enzyme."
        p_fri = "Fatty fish (Salmon/Saba) + 1g supplement."
        p_sun = "Hot Bath + 5min cold shower for recovery."
    else: # 上級
        p_mon = "18:6 Fasting. Advanced EGCG flux optimization."
        p_tue = "Symbiotic loading: Fermented foods + Prebiotic fibers."
        p_wed = "Diversity loading: 3+ types of Seaweed & Sea vegetables."
        p_fri = "High-grade Sashimi. Precision Omega-3 timing."
        p_sun = "Sauna + Ice Bath (Full HSP/Cold-shock activation)."

    # 03 Protocol Table
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(accent)
    c.drawString(margin, height - 4.3*inch, "03 // PERSONALIZED PROTOCOL")
    data = [
        ['Day', 'Focus', 'Action'],
        ['Mon', 'Autophagy', Paragraph(p_mon, styleN)],
        ['Tue', 'Microbiome', Paragraph(p_tue, styleN)],
        ['Wed', 'Enzyme', Paragraph(p_wed, styleN)],
        ['Thu', 'Recovery', Paragraph('2g Ippodo Matcha. Prioritize L-Theanine.', styleN)],
        ['Fri', 'Omega-3', Paragraph(p_fri, styleN)],
        ['Sat', 'Metabolism', Paragraph('HIIT Session. Activate glycolysis.', styleN)],
        ['Sun', 'Rest', Paragraph(p_sun, styleN)]
    ]
    table = Table(data, colWidths=[0.7*inch, 1.1*inch, 4.4*inch], rowHeights=0.4*inch)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, margin, height - 8.2*inch)

    c.showPage() # --- PAGE 2 ---
    c.setFillColorRGB(0.05, 0.05, 0.05)
    c.rect(0, 0, width, height, fill=True)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(accent)
    c.drawString(margin, height - 1.8*inch, "04 // THE GOLD STANDARD STACK")
    
    y = height - 2.3*inch
    stack = [
        ("Ippodo Matcha", LINKS['matcha'], "Finest L-Theanine source."),
        ("Suntory NMN", LINKS['nmn'], "99.9% purity for DNA repair."),
        ("Spermidine", LINKS['spermidine'], "Autophagy inducer."),
        ("EPA / DHA", LINKS['omega3'], "Inflammation control."),
        ("Zojirushi IH", LINKS['cooker'], "Metabolism foundation.")
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

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='ZENGEN_Premium_Report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)