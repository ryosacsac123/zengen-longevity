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

def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Page 1: Background & Header ---
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "OFFICIAL LONGEVITY BLUEPRINT")
    
    # Score Circle
    p.setStrokeColor(colors.HexColor("#39FF14"))
    p.setLineWidth(3)
    p.circle(width/2, height - 150, 70, stroke=1, fill=0)
    
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 165, f"{score}/8")
    
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawCentredString(width/2, height - 240, "JDI8 SCORE")
    
    # --- Risk Assessment Logic (3-Tier) ---
    if score <= 3:
        risk_text = "RISK ASSESSMENT: HIGH"
    elif score <= 6:
        risk_text = "RISK ASSESSMENT: MODERATE"
    else:
        risk_text = "RISK ASSESSMENT: LOW"

    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 270, risk_text)

    # Section 02: Genetic Edge
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 330, "02 // THE JAPANESE GENETIC EDGE")
    
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.white)
    p.drawString(40, height - 350, "Nature (2010): Porphyranase enzyme pathway identified for marine processing.")

    # Section 03: Protocol
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 390, "03 // PERSONALIZED PROTOCOL")

    # Dynamic Table Data based on Score
    if score <= 4:
        data = [
            ["Day", "Focus", "Action"],
            ["Mon", "Autophagy", "Hydration focus. Start with Miso soup to reset."],
            ["Tue", "Microbiome", "Eat Natto at dinner to support mucosa."],
            ["Wed", "Enzyme", "Seaweed side dish. Support marine polysaccharide digestion."], # 更新箇所
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
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
    ]))
    
    table.wrapOn(p, 40, 420)
    table.drawOn(p, 40, height - 600)

    p.showPage() # Page 2

    # --- Page 2: Stocks ---
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

@app.route('/download-report')
def download_report():
    score = int(request.args.get('score', 0))
    pdf_buffer = create_report(score)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"ZENGEN_Premium_Report_{score}.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
   @app.route('/legal')
def legal():
    return """
    <html>
    <head>
        <title>Commerce Disclosure - ZENGEN AI</title>
        <meta name="robots" content="noindex, nofollow">
        <style>
            body { font-family: sans-serif; background-color: #000; color: #fff; padding: 40px; line-height: 1.8; }
            h1 { color: #39FF14; border-bottom: 1px solid #333; }
            .label { color: #39FF14; font-weight: bold; width: 150px; display: inline-block; }
            a { color: #39FF14; text-decoration: none; border: 1px solid #39FF14; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>特定商取引法に基づく表記</h1>
        <p><span class="label">販売業者:</span> 佐久間稜</p>
        <p><span class="label">所在地:</span> 〒060-0813 北海道札幌市北区北13条西8丁目 北海道大学大学院 工学院</p>
        <p><span class="label">電話番号:</span> 090-6446-6654</p>
        <p><span class="label">メールアドレス:</span> ryo1ryo2-1103@outlook.jp</p>
        <p><span class="label">販売価格:</span> $5.00</p>
        <p><span class="label">支払方法:</span> クレジットカード (Stripe)</p>
        <p><span class="label">商品引渡時期:</span> 決済完了後、即時にPDFレポートを生成・表示</p>
        <p><span class="label">返品・返金:</span> デジタルコンテンツの特性上、返品・返金には応じられません。</p>
        <br><br>
        <a href="/">診断に戻る / Back to Home</a>
    </body>
    </html>
    """