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

# --- 1. Diagnosis Service Logic (PDF Generation) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Page 1: Design & Score
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "OFFICIAL LONGEVITY BLUEPRINT")
    
    p.setStrokeColor(colors.HexColor("#39FF14"))
    p.setLineWidth(3)
    p.circle(width/2, height - 150, 70, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 165, f"{score}/8")
    
    if score <= 3: risk_text = "RISK ASSESSMENT: HIGH"
    elif score <= 6: risk_text = "RISK ASSESSMENT: MODERATE"
    else: risk_text = "RISK ASSESSMENT: LOW"
    
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 270, risk_text)

    # Protocol Table
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 390, "03 // PERSONALIZED PROTOCOL")

    seaweed_action = "Seaweed side dish. Support marine polysaccharide digestion."
    if score <= 4:
        data = [
            ["Day", "Focus", "Action"],
            ["Mon", "Autophagy", "Hydration focus. Start with Miso soup to reset."],
            ["Tue", "Microbiome", "Eat Natto at dinner to support mucosa."],
            ["Wed", "Enzyme", seaweed_action],
            ["Thu", "Recovery", "2g Ippodo Matcha. Prioritize L-Theanine."],
            ["Fri", "Omega-3", "Omega-3: Take 1g EPA/DHA supplement."],
            ["Sat", "Metabolism", "HIIT Session. Activate glycolysis."],
            ["Sun", "Rest", "Focus on 20min hot soak to activate HSP."]
        ]
    else:
        data = [
            ["Day", "Focus", "Action"],
            ["Mon", "Autophagy", "16:8 Fasting. Break fast with Miso & Seaweed."],
            ["Tue", "Microbiome", "Microbiome Diversity: Mix Natto with Okra/Kimchi."],
            ["Wed", "Enzyme", "Seaweed Salad. Support marine polysaccharide digestion."],
            ["Thu", "Nootropic", "2g Ippodo Matcha. Prioritize L-Theanine."],
            ["Fri", "Omega-3", "Fatty fish (Salmon/Saba) + 1g supplement."],
            ["Sat", "Metabolism", "HIIT Session. Activate glycolysis."],
            ["Sun", "Rest", "Hot Bath + 5min cold shower for recovery."]
        ]

    table = Table(data, colWidths=[50, 80, 380])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#39FF14")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
    ]))
    table.wrapOn(p, 40, 420)
    table.drawOn(p, 40, height - 600)

    p.showPage() # Page 2: Stack & Links
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "04 // THE GOLD STANDARD STACK")

    y_pos = height - 80
    items = [
        ("Ippodo Matcha", "Finest L-Theanine source.", LINKS["Ippodo Matcha"]),
        ("NMN", "NAD+ precursor for DNA repair and cellular energy.", LINKS["NMN"]),
        ("Spermidine", "Autophagy inducer.", LINKS["Spermidine"]),
        ("EPA/DHA", "Inflammation control.", LINKS["EPA/DHA"]),
        ("Zojirushi IH", "Metabolism foundation.", LINKS["Zojirushi IH"])
    ]

    for title, desc, link in items:
        p.setFont("Helvetica-Bold", 11)
        p.setFillColor(colors.white)
        p.drawString(40, y_pos, f"> {title}:")
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.lightgrey)
        p.drawString(50, y_pos - 15, desc)
        p.setFont("Helvetica-Oblique", 9)
        p.setFillColor(colors.HexColor("#39FF14"))
        p.drawString(50, y_pos - 30, f"View on Amazon: {link}")
        y_pos -= 60

    p.save()
    buffer.seek(0)
    return buffer

# --- 2. Website Routes (Home & Legal) ---

@app.route('/')
def home():
    # 診断サービス自体を表示するメイン画面です
    return """
    <html>
    <head>
        <title>ZENGEN AI - Longevity Blueprint</title>
        <style>
            body { background-color: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 50px; }
            h1 { color: #39FF14; font-size: 3rem; letter-spacing: 4px; margin-bottom: 10px; }
            p { font-style: italic; color: #888; margin-bottom: 40px; }
            .container { max-width: 500px; margin: 0 auto; background: #111; padding: 30px; border-radius: 15px; border: 1px solid #333; text-align: left; }
            .q { margin-bottom: 15px; font-size: 1.1rem; display: flex; align-items: center; }
            input[type="checkbox"] { transform: scale(1.5); margin-right: 15px; accent-color: #39FF14; }
            button { width: 100%; background: #39FF14; color: #000; border: none; padding: 20px; font-weight: bold; font-size: 1.2rem; cursor: pointer; border-radius: 5px; margin-top: 20px; }
            footer { margin-top: 60px; font-size: 0.8rem; }
            footer a { color: #444; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>ZENGEN AI</h1>
        <p>Personalized Longevity Protocol Engine</p>
        <div class="container">
            <div class="q"><input type="checkbox" class="jdi"> Rice (Daily)</div>
            <div class="q"><input type="checkbox" class="jdi"> Miso Soup (Daily)</div>
            <div class="q"><input type="checkbox" class="jdi"> Seaweed (Daily)</div>
            <div class="q"><input type="checkbox" class="jdi"> Pickles (Daily)</div>
            <div class="q"><input type="checkbox" class="jdi"> Green/Yellow Vegetables (Daily)</div>
            <div class="q"><input type="checkbox" class="jdi"> Fish (Daily)</div>
            <div class="q"><input type="checkbox" class="jdi"> Green Tea (Daily)</div>
            <div class="q"><input type="checkbox" class="jdi"> Less Beef/Pork consumption</div>
            <button onclick="calc()">GET PREMIUM REPORT ($5)</button>
        </div>
        <script>
            function calc() {
                let s = document.querySelectorAll('.jdi:checked').length;
                window.location.href = `/download-report?score=${s}`;
            }
        </script>
        <footer>
            <a href="/legal">Commerce Disclosure (特定商取引法に基づく表記)</a>
        </footer>
    </body>
    </html>
    """

@app.route('/download-report')
def download_report():
    score = int(request.args.get('score', 0))
    pdf_buffer = create_report(score)
    return send_file(pdf_buffer, as_attachment=True, download_name=f"ZENGEN_Report_{score}.pdf", mimetype='application/pdf')

@app.route('/legal')
def legal():
    return """
    <html>
    <head><title>Legal - ZENGEN AI</title><meta name="robots" content="noindex"></head>
    <body style="background:#000; color:#fff; font-family:sans-serif; padding:40px; line-height:1.8;">
        <h1 style="color:#39FF14;">特定商取引法に基づく表記</h1>
        <p><b>販売業者:</b> 佐久間稜</p>
        <p><b>所在地:</b> 〒060-0813 北海道札幌市北区北13条西8丁目 北海道大学大学院 工学院</p>
        <p><b>電話番号:</b> 090-6446-6654</p>
        <p><b>メールアドレス:</b> ryo1ryo2-1103@outlook.jp</p>
        <p><b>販売価格:</b> $5.00</p>
        <p><b>支払方法:</b> クレジットカード (Stripe)</p>
        <p><b>商品引渡時期:</b> 決済完了後、即時にPDFレポートを表示</p>
        <br><a href="/" style="color:#39FF14; text-decoration:none; border:1px solid #39FF14; padding:10px;">診断に戻る</a>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)