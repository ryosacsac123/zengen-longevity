from flask import Flask, send_file, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
import io

app = Flask(__name__)

# --- Amazon Affiliate Links ---
LINKS = {
    "Ippodo Matcha": "https://amzn.to/3ZgMv0Q",
    "NMN": "https://amzn.to/4qTcOHM",
    "Spermidine": "https://amzn.to/4tYE6j2",
    "EPA/DHA": "https://amzn.to/4kRTklz",
    "Zojirushi IH": "https://amzn.to/4hfC1sA"
}

# --- PDF Generation Engine ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    
    # Score Display
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 165, f"{score}/8")
    
    # Risk Assessment
    if score <= 3: risk_text = "RISK ASSESSMENT: HIGH"
    elif score <= 6: risk_text = "RISK ASSESSMENT: MODERATE"
    else: risk_text = "RISK ASSESSMENT: LOW"
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 270, risk_text)

    # Protocol Table
    seaweed = "Seaweed side dish. Support marine polysaccharide digestion."
    data = [["Day", "Focus", "Action"]]
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        action = seaweed if day == "Wed" else "Optimized protocol details..."
        data.append([day, "Longevity", action])

    table = Table(data, colWidths=[50, 80, 380])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
    ]))
    table.wrapOn(p, 40, 420)
    table.drawOn(p, 40, height - 600)
    
    p.showPage() # Page 2: Links
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    y = height - 80
    for item, desc, link in [("NMN", "Cellular energy.", LINKS["NMN"]), ("Matcha", "L-Theanine.", LINKS["Ippodo Matcha"])]:
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(colors.white)
        p.drawString(40, y, f"> {item}: {desc}")
        p.setFont("Helvetica-Oblique", 9)
        p.setFillColor(colors.HexColor("#39FF14"))
        p.drawString(50, y - 20, f"View on Amazon: {link}")
        y -= 50

    p.save()
    buffer.seek(0)
    return buffer

# --- Routes ---

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>ZENGEN AI - Longevity Blueprint</title>
        <style>
            body { background-color: #000; color: #fff; font-family: 'Helvetica', sans-serif; padding: 20px; text-align: center; }
            h1 { color: #39FF14; letter-spacing: 3px; margin-top: 50px; }
            .card { background: #111; border: 1px solid #333; padding: 30px; border-radius: 15px; max-width: 500px; margin: 40px auto; text-align: left; }
            .q-item { margin-bottom: 15px; display: flex; align-items: center; font-size: 1.1rem; }
            input[type='checkbox'] { transform: scale(1.5); margin-right: 15px; accent-color: #39FF14; }
            button { background: #39FF14; color: #000; border: none; padding: 15px 30px; font-weight: bold; border-radius: 5px; cursor: pointer; width: 100%; font-size: 1.1rem; margin-top: 20px; }
            .footer { margin-top: 50px; font-size: 0.8rem; }
            .footer a { color: #555; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>ZENGEN AI</h1>
        <p>Japanese Dietary Index 8 (JDI8) Diagnosis</p>
        
        <div class="card">
            <div class="q-item"><input type="checkbox" class="jdi"> Rice (Daily)</div>
            <div class="q-item"><input type="checkbox" class="jdi"> Miso Soup (Daily)</div>
            <div class="q-item"><input type="checkbox" class="jdi"> Seaweed (Daily)</div>
            <div class="q-item"><input type="checkbox" class="jdi"> Pickles (Daily)</div>
            <div class="q-item"><input type="checkbox" class="jdi"> Green & Yellow Vegetables (Daily)</div>
            <div class="q-item"><input type="checkbox" class="jdi"> Fish (Daily)</div>
            <div class="q-item"><input type="checkbox" class="jdi"> Green Tea (Daily)</div>
            <div class="q-item"><input type="checkbox" class="jdi-inv"> Beef/Pork (Less than once a week)</div>
            
            <button onclick="calculate()">GET MY BLUEPRINT ($5)</button>
        </div>

        <script>
            function calculate() {
                let score = 0;
                document.querySelectorAll('.jdi').forEach(cb => { if(cb.checked) score++; });
                if(document.querySelector('.jdi-inv').checked) score++;
                
                // 本来はここでStripeへ。一旦、直接PDFへ。
                window.location.href = `/download-report?score=${score}`;
            }
        </script>

        <div class="footer">
            <a href="/legal">Commerce Disclosure (特定商取引法に基づく表記)</a>
        </div>
    </body>
    </html>
    """

@app.route('/download-report')
def download_report():
    score = int(request.args.get('score', 0))
    return send_file(create_report(score), as_attachment=True, download_name=f"ZENGEN_Report_{score}.pdf", mimetype='application/pdf')

@app.route('/legal')
def legal():
    # 前回の特商法コードをここに維持（省略）
    return "Legal content here (佐久間稜 / 北海道大学...)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))