import os
import io
import stripe
from flask import Flask, send_file, request, jsonify, redirect
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

app = Flask(__name__)

# --- CONFIGURATION ---
# Set to True to skip Stripe for testing. Set to False for real Stripe review.
DEBUG_MODE = True 

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_placeholder")

# --- 1. RICH PDF ENGINE (Faithful restoration of the 2-page format) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- PAGE 1: DIAGNOSIS & PROTOCOL --- [cite: 7-14]
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "OFFICIAL LONGEVITY BLUEPRINT")
    
    # Biometric Score Circle
    p.setStrokeColor(colors.HexColor("#39FF14"))
    p.setLineWidth(3)
    p.circle(width/2, height - 150, 70, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 165, f"{score}/8")
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawCentredString(width/2, height - 240, "JDI8 SCORE")
    
    risk = "HIGH" if score <= 4 else "MODERATE"
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 270, f"RISK ASSESSMENT: {risk}")

    # Science Section [cite: 6, 29]
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 330, "02 // THE JAPANESE GENETIC EDGE")
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.white)
    p.drawString(40, height - 350, "Nature (2010): Porphyranase enzyme pathway identified for marine processing.")

    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 390, "03 // PERSONALIZED PROTOCOL")

    # Detailed Table Restoration [cite: 7, 31]
    data = [["Day", "Focus", "Action"]]
    if score <= 4:
        rows = [
            ["Mon", "Autophagy", "Hydration focus. Start with Miso soup to reset."],
            ["Tue", "Microbiome", "Eat Natto at dinner to support mucosa."],
            ["Wed", "Enzyme", "Seaweed side dish. Support marine digestion."],
            ["Thu", "Recovery", "2g Ippodo Matcha. Prioritize L-Theanine."],
            ["Fri", "Omega-3", "Take 1g EPA/DHA supplement."],
            ["Sat", "Metabolism", "HIIT Session. Activate glycolysis."],
            ["Sun", "Rest", "20min hot soak to activate HSP."]
        ]
    else:
        rows = [
            ["Mon", "Autophagy", "16:8 Fasting. Break fast with Miso & Seaweed."],
            ["Tue", "Microbiome", "Mix Natto with Okra/Kimchi."],
            ["Wed", "Enzyme", "Seaweed Salad. Activate Porphyranase enzyme."],
            ["Thu", "Nootropic", "2g Ippodo Matcha. Prioritize L-Theanine."],
            ["Fri", "Omega-3", "Fatty fish (Salmon/Saba) + 1g supplement."],
            ["Sat", "Metabolism", "HIIT Session. Activate glycolysis."],
            ["Sun", "Rest", "Hot Bath + 5min cold shower for recovery."]
        ]
    for r in rows: data.append(r)

    table = Table(data, colWidths=[50, 80, 380])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#39FF14")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    table.wrapOn(p, 40, 420)
    table.drawOn(p, 40, height - 600)

    # --- PAGE 2: THE GOLD STANDARD STACK --- [cite: 8-23, 32-42]
    p.showPage()
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "04 // THE GOLD STANDARD STACK")

    stacks = [
        ("Ippodo Matcha", "Finest L-Theanine source.", "https://amzn.to/3ZgMv0Q"),
        ("NMN", "NAD+ precursor for DNA repair.", "https://amzn.to/4qTcOHM"),
        ("Spermidine", "Autophagy inducer.", "https://amzn.to/4tYE6j2"),
        ("EPA/DHA", "Inflammation control.", "https://amzn.to/4kRTklz"),
        ("Zojirushi IH", "Metabolism foundation.", "https://amzn.to/4hfC1sA")
    ]
    y = height - 80
    for title, desc, link in stacks:
        p.setFont("Helvetica-Bold", 11)
        p.setFillColor(colors.white)
        p.drawString(40, y, f"> {title}:")
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.lightgrey)
        p.drawString(50, y - 15, desc)
        p.setFont("Helvetica-Oblique", 9)
        p.setFillColor(colors.HexColor("#39FF14"))
        p.drawString(50, y - 30, f"View on Amazon: {link}")
        y -= 60
    
    p.save()
    buffer.seek(0)
    return buffer

# --- 2. SECURE WEB INTERFACE (Non-f-string to avoid SyntaxErrors) ---

@app.route('/')
def home():
    debug_js = "true" if DEBUG_MODE else "false"
    # Using a standard string and .replace() to avoid f-string brace issues
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>ZENGEN AI | Longevity</title>
        <style>
            :root { --neon: #39FF14; --bg: #000; }
            body { margin:0; overflow:hidden; background:var(--bg); color:#fff; font-family:sans-serif; }
            #canvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1; filter:blur(40px); opacity:0.8; }
            .screen { position:absolute; width:100vw; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; transition:0.9s cubic-bezier(0.8, 0, 0.2, 1); }
            #page1 { transform:translateX(0); }
            #page2 { transform:translateX(100%); }
            #page3 { transform:translateX(100%); }
            h1 { font-size:6.5rem; letter-spacing:25px; color:var(--neon); font-weight:100; margin:0; text-shadow:0 0 35px var(--neon); cursor:pointer; }
            .card { background:rgba(10,10,10,0.85); border:1px solid #222; padding:50px; border-radius:35px; backdrop-filter:blur(30px); width:540px; box-shadow:0 60px 120px #000; position:relative; }
            .section-label { color:var(--neon); font-size:0.7rem; letter-spacing:5px; margin-bottom:20px; text-transform:uppercase; border-bottom:1px solid #222; padding-bottom:10px; }
            .q-item { margin-bottom:15px; display:flex; align-items:center; font-size:1.1rem; letter-spacing:1px; color:#ccc; }
            input[type="checkbox"] { transform:scale(1.6); margin-right:20px; accent-color:var(--neon); cursor:pointer; }
            button { background:transparent; color:var(--neon); border:1px solid var(--neon); padding:20px 70px; font-weight:bold; cursor:pointer; letter-spacing:7px; transition:0.6s; margin-top:40px; text-transform:uppercase; font-size:0.95rem; }
            button:hover { background:var(--neon); color:#000; box-shadow:0 0 50px var(--neon); }
            .summary-box { border: 1px dashed var(--neon); padding: 25px; border-radius: 15px; margin: 30px 0; text-align: left; background: rgba(57, 255, 20, 0.04); }
            .val-list { list-style: none; padding: 0; color: #888; font-size: 0.95rem; line-height: 2.2; }
            .val-list span { color: var(--neon); }
            .disclaimer { position:absolute; bottom:20px; width:100%; text-align:center; font-size:0.55rem; color:#444; letter-spacing:1px; }
        </style>
    </head>
    <body>
        <canvas id="canvas"></canvas>
        <div id="page1" class="screen">
            <h1 onclick="move(1,2)">ZENGEN</h1>
            <div style="color:#444; letter-spacing:10px; margin-top:20px; font-size:0.8rem; text-transform:uppercase;">Longevity Architecture</div>
            <button onclick="move(1,2)">Initiate Analysis</button>
            <div class="disclaimer">ADVICE ONLY. NOT A MEDICAL DIAGNOSIS.</div>
        </div>
        <div id="page2" class="screen">
            <div class="card">
                <div class="section-label">02 // BIOMETRIC INPUT</div>
                <div class="q-item"><input type="checkbox" class="j"> RICE (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> MISO SOUP (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> SEAWEED (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> PICKLES (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> GREEN & YELLOW VEG</div>
                <div class="q-item"><input type="checkbox" class="j"> FISH (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> GREEN TEA (DAILY)</div>
                <div class="section-label" style="margin-top:30px;">02b // INVERSE FACTOR</div>
                <div class="q-item"><input type="checkbox" class="j-inv"> LOW BEEF/PORK INTAKE</div>
                <button onclick="move(2,3)" style="width:100%;">Synthesize</button>
                <div style="margin-top:25px; font-size:0.7rem;"><a href="/about" style="color:#333; text-decoration:none;">ABOUT US</a> | <a href="/legal" style="color:#333; text-decoration:none;">COMMERCE DISCLOSURE</a></div>
            </div>
            <div class="disclaimer">ADVICE ONLY. NOT A MEDICAL DIAGNOSIS.</div>
        </div>
        <div id="page3" class="screen">
            <div class="card" style="text-align:center;">
                <div class="section-label">03 // ANALYSIS READY</div>
                <h2 style="letter-spacing:10px; font-weight:100; font-size:2rem; margin:0;">BLUEPRINT READY</h2>
                <div class="summary-box">
                    <div style="font-size: 1.5rem; letter-spacing: 2px;">Your JDI8 Score: <span id="dispScore" style="color:var(--neon); font-weight:bold;">0</span>/8</div>
                    <ul class="val-list">
                        <li>● <span>7-Day</span> Optimized Biological Protocol</li>
                        <li>● <span>Porphyranase</span> Enzyme Synthesis Pathway</li>
                        <li>● <span>Gold Standard</span> Stack for DNA Repair</li>
                    </ul>
                </div>
                <button onclick="toPayment()" style="width:100%; border:none; background:var(--neon); color:#000;">Unlock Full Access ($5.00)</button>
            </div>
            <div class="disclaimer">ADVICE ONLY. NOT A MEDICAL DIAGNOSIS.</div>
        </div>
        <footer><div style="position:fixed; bottom:30px; width:100%; text-align:center; font-size:0.6rem; letter-spacing:4px;"><a href="/legal" style="color:#333; text-decoration:none; margin:0 20px;">LEGAL</a><a href="/about" style="color:#333; text-decoration:none; margin:0 20px;">ABOUT US</a></div></footer>
        <script>
            const canvas = document.getElementById('canvas'); const ctx = canvas.getContext('2d');
            let w, h, orbs = [], state = "dance", debug = DEBUG_REPLACE;
            function init() {
                w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight;
                orbs = []; for(let i=0; i<15; i++) orbs.push({x:Math.random()*w, y:Math.random()*h, r:Math.random()*200+100, v:{x:(Math.random()-0.5)*0.6, y:(Math.random()-0.5)*0.6}});
            }
            function draw() {
                ctx.clearRect(0,0,w,h);
                orbs.forEach(o => {
                    if(state === "dance") { o.x += o.v.x; o.y += o.v.y; if(o.x<0||o.x>w) o.v.x*=-1; if(o.y<0||o.y>h) o.v.y*=-1; }
                    else { o.x += (w/2 - o.x) * 0.02; o.y += (h/2 - o.y) * 0.02; o.r += (150 - o.r) * 0.01; }
                    let g = ctx.createRadialGradient(o.x,o.y,0,o.x,o.y,o.r); g.addColorStop(0,'rgba(57,255,20,0.4)'); g.addColorStop(1,'rgba(0,0,0,0)');
                    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(o.x,o.y,o.r,0,Math.PI*2); ctx.fill();
                }); requestAnimationFrame(draw);
            }
            init(); draw();
            function move(f, t) {
                if(f===1) state = "converge"; 
                let s = document.querySelectorAll('.j:checked').length + document.querySelectorAll('.j-inv:checked').length;
                document.getElementById('dispScore').innerText = s;
                document.getElementById('page'+f).style.transform = 'translateX(-100%)';
                document.getElementById('page'+t).style.transform = 'translateX(0)';
            }
            function toPayment() {
                let s = document.getElementById('dispScore').innerText;
                if(debug) { window.location.href='/download-report?score=' + s; }
                else {
                    let form = document.createElement('form'); form.method='POST'; form.action='/create-checkout-session';
                    let input = document.createElement('input'); input.type='hidden'; input.name='score'; input.value=s;
                    form.appendChild(input); document.body.appendChild(form); form.submit();
                }
            }
        </script>
    </body>
    </html>
    """.replace("DEBUG_REPLACE", debug_js)
    return html

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    score = request.form.get('score', 0)
    try:
        session = stripe.checkout.Session.create(
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': 'ZENGEN Longevity Blueprint'}, 'unit_amount': 500}, 'quantity': 1}],
            mode='payment',
            success_url=request.host_url + f'success?score={score}',
            cancel_url=request.host_url,
        )
        return redirect(session.url, code=303)
    except Exception as e: return str(e), 500

@app.route('/success')
def success():
    score = request.args.get('score', 0)
    return f"""
    <body style="background:#000; color:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; font-family:sans-serif; margin:0;">
        <h2 style="color:#39FF14; letter-spacing:5px;">PAYMENT SUCCESSFUL</h2>
        <a href="/download-report?score={score}" style="text-decoration:none; background:#39FF14; color:#000; padding:20px 40px; font-weight:bold; border-radius:5px; margin-top:30px;">
            DOWNLOAD OFFICIAL LONGEVITY BLUEPRINT
        </a>
    </body>
    """

@app.route('/download-report')
def download_report():
    try:
        score = int(request.args.get('score', 0))
        return send_file(create_report(score), as_attachment=True, download_name=f"ZENGEN_Official_Report.pdf", mimetype='application/pdf')
    except Exception as e: return f"Internal Error: {str(e)}", 500

@app.route('/about')
def about():
    return """<body style="background:#000;color:#fff;padding:80px;font-family:sans-serif;line-height:2.8;"><h1 style="color:#39FF14;">ABOUT US</h1><p>Curated by Ryoh Sakuma, Hokkaido University Graduate School of Engineering. Biological architecture for longevity.</p><a href="/" style="color:#39FF14; text-decoration:none; border:1px solid #39FF14; padding:10px 20px;">BACK</a></body>"""

@app.route('/legal')
def legal():
    return """<body style="background:#000;color:#fff;padding:80px;font-family:sans-serif;line-height:2.8;"><h1 style="color:#39FF14;">COMMERCE DISCLOSURE</h1><p>Merchant: Ryoh Sakuma<br>Location: Sapporo, Hokkaido, Japan (Hokkaido University)<br>Price: $5.00<br>Refund Policy: No refunds on digital content.<br>Contact: ryo1ryo2-1103@outlook.jp</p><a href="/" style="color:#39FF14; text-decoration:none; border:1px solid #39FF14; padding:10px 20px;">BACK</a></body>"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)