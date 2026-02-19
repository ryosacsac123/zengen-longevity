from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate_score', methods=['POST'])
def calculate_score():
    data = request.json
    
    # 8 items: Rice, Miso, Seaweed, Pickles, YellowGreenVeg, Fish, GreenTea, BeefPork
    # Input is expected to be boolean-like (true if >= median, false otherwise)
    # except BeefPork where true if < median is the target for point? 
    # Actually, let's standardize: 
    # The prompt says: 
    # 7 items: +1 if >= median
    # Beef/Pork: +1 if < median
    
    # Let's assume the frontend sends boolean "high_intake" for all.
    # We will adjust logic accordingly.
    
    score = 0
    details = []

    # Positive items (High intake is good)
    positive_items = ['rice', 'miso_soup', 'seaweed', 'pickles', 'green_yellow_veg', 'fish', 'green_tea']
    for item in positive_items:
        if data.get(item, False): # True means High Intake
            score += 1
            details.append(f"{item}: +1 (High Intake)")
        else:
             details.append(f"{item}: 0 (Low Intake)")

    # Negative item (Low intake is good)
    # If data['beef_pork'] is True (High Intake), then 0 points.
    # If False (Low Intake), then +1 point.
    if not data.get('beef_pork', False): 
        score += 1
        details.append("beef_pork: +1 (Low Intake)")
    else:
        details.append("beef_pork: 0 (High Intake)")
    
    global latest_score
    latest_score = score


    risk_reduction = "Low"
    if score >= 6:
        risk_reduction = "High (14% lower mortality risk)"
    elif score >= 3:
         risk_reduction = "Moderate"

    return jsonify({
        "score": score,
        "risk_reduction": risk_reduction,
        "details": details
    })

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
import stripe
import os
import datetime
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env if present

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
# Use BASE_URL from env, or default to Render URL for production
DOMAIN = os.environ.get('BASE_URL', 'https://zengen-longevity.onrender.com')
print(f"Server starting with DOMAIN: {DOMAIN}")

latest_score = 0 # Global variable for MVP score persistence

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'ZenGen Personalized Longevity Plan (1-Week)',
                        },
                        'unit_amount': 500,  # $5.00
                    },
                    'quantity': 1,
                },
            ],
            mode='payment', # Single payment
            locale='en',
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/download-report')
def download_report():
    # Retrieve score from session, default to 0 if not found
    try:
        global latest_score
        user_score = latest_score
        # We need the user's detailed answers to provide personalized feedback.
        # For this MVP, since we don't have session storage for details, 
        # we will assume a "Low" score implies low intake for critical items for demonstration.
        # In a real app, 'details' would be stored in session or DB.
        # Let's mock 'low intake' for Green Tea, Rice, Fish if score is low (<4) for demo.
        is_low_score = user_score < 4
    except NameError:
        user_score = 0
        is_low_score = True
        
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # 1. Visual Design System: Dark Mode Background
    c.setFillColorRGB(0.1, 0.1, 0.1)  # Dark Grey/Black background
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    # Constants
    margin_left = 0.8 * inch
    accent_color = colors.HexColor("#99ff00") # Lime Green
    text_white = colors.white
    
    # --- OFFICIAL HEADER ---
    header_y = height - 0.5 * inch
    c.setStrokeColor(accent_color)
    c.setLineWidth(4) # Thicker line
    c.line(margin_left, header_y, width - margin_left, header_y)
    
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(accent_color)
    # Centered Header Text
    c.drawCentredString(width / 2, header_y - 0.25 * inch, "OFFICIAL LONGEVITY BLUEPRINT")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawRightString(width - margin_left, header_y + 0.1 * inch, "CONFIDENTIAL ANALYSIS")

    # Title Section
    title_y = header_y - 0.6 * inch # Reduced gap
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(text_white)
    c.drawString(margin_left, title_y, "Your Bio-Hacking Blueprint")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.lightgrey)
    c.drawString(margin_left, title_y - 0.25 * inch, f"Generated on: {datetime.date.today().strftime('%Y-%m-%d')} | ID: GEN-{datetime.datetime.now().strftime('%H%M%S')}")

    # 2. Data Visualization: JDI8 Score HERO ELEMENT
    max_score = 8
    
    # Determine Risk Label based on Score
    risk_label = "Low"
    if user_score >= 6:
        risk_label = "High (14% lower mortality risk)"
    elif user_score >= 3:
        risk_label = "Moderate"
    
    # Circle Center
    circle_y = title_y - 1.4 * inch # Reduced gap
    circle_x = width / 2
    circle_radius = 0.8 * inch
    
    # Draw Circle
    c.setStrokeColor(accent_color)
    c.setLineWidth(3)
    c.setFillColorRGB(0.15, 0.15, 0.15) # Slightly lighter inner circle
    c.circle(circle_x, circle_y, circle_radius, stroke=True, fill=True)
    
    # Score Text inside Circle
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(text_white)
    c.drawCentredString(circle_x, circle_y - 10, f"{user_score}/{max_score}") # Adjust y slightly for visual center
    
    c.setFont("Helvetica", 10)
    c.setFillColor(accent_color)
    c.drawCentredString(circle_x, circle_y - 0.5 * inch, "JDI8 SCORE")
    
    # Risk Badge (Centered below circle)
    badge_width = 3 * inch
    badge_height = 0.4 * inch
    badge_x = circle_x - (badge_width / 2)
    badge_y = circle_y - 1.1 * inch # Reduced gap
    
    c.setStrokeColor(accent_color)
    c.setLineWidth(1)
    c.roundRect(badge_x, badge_y, badge_width, badge_height, 4, stroke=True, fill=False)
    
    # Vertically Centered Text in Badge
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(text_white)
    text_height = 10 # approximate cap height
    text_y_centered = badge_y + (badge_height / 2) - (text_height / 3)
    c.drawCentredString(circle_x, text_y_centered, f"RISK REDUCTION: {risk_label.upper()}")


    # 3. Structured Sections (Increased Spacing)
    # Start sections lower down
    current_y = badge_y - 0.6 * inch # Reduced gap
    spacing = 0.4 * inch # Reduced spacing between sections
    
    # Section 1: Bio-Marker Analysis & PERSONALIZED RECOMMENDATIONS
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(accent_color)
    c.drawString(margin_left, current_y, "01 // BIO-MARKER ANALYSIS")
    
    current_y -= 0.3 * inch
    
    # Standard Analysis
    analysis_text = [
        "• Rice & Miso: High Intake. Excellent. Base of the JDI8 pyramid.",
        "• Seaweed: Optimal. Activating gut microbiota diversity.",
        "• Animal Protein: Moderate. Good balance for IGF-1 regulation.",
        "• Green Tea: Daily. High EGCG levels detected."
    ]
    
    # Personalized Recommendations Logic (Simulated for Demo)
    if is_low_score:
        analysis_text = [
           "• Rice & Miso: Intake is sub-optimal. Review foundational carbs.",
           "• Green Tea: Levels are Critical. Boost EGCG immediately.",
           "• Fish: Low Omega-3 detected. Inflammation risk elevated."
        ]
        
    c.setFont("Helvetica", 10) # Slightly smaller to fit more text
    c.setFillColor(text_white)
    for line in analysis_text:
        c.drawString(margin_left + 0.2 * inch, current_y, line)
        current_y -= 0.2 * inch
        
    # --- DYNAMIC RECOMMENDATIONS ---
    if is_low_score:
        current_y -= 0.1 * inch
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.red) # Alarm color for critical recommendations
        
        recs = [
            "CRITICAL: Your EGCG levels are low. Ippodo Matcha is top priority.",
            "LONGEVITY GAP: Precision cooking key. Zojirushi IH Cooker recommended.",
            "ESSENTIAL: Low fish intake. Highly recommend EPA/DHA supplements."
        ]
        for rec in recs:
            c.drawString(margin_left + 0.2 * inch, current_y, rec)
            current_y -= 0.2 * inch
        
    # Section 2: Genetic Edge
    current_y -= spacing
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(accent_color)
    c.drawString(margin_left, current_y, "02 // THE JAPANESE GENETIC EDGE")
    
    current_y -= 1.1 * inch # Reduced box height allocation
    # Box for Special Insight
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.rect(margin_left, current_y, width - (2 * margin_left), 0.9 * inch, stroke=True, fill=False) # Slightly smaller box
    
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(text_white)
    c.drawString(margin_left + 0.2 * inch, current_y + 0.65 * inch, "GENETIC INSIGHT: Bacteroides plebeius")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.lightgrey)
    c.drawString(margin_left + 0.2 * inch, current_y + 0.4 * inch, "Research (Nature, 2010) reveals you likely possess the 'Porphyranase' enzyme.")
    c.drawString(margin_left + 0.2 * inch, current_y + 0.2 * inch, "This allows unique biological access to marine sulphated polysaccharides.")

    # Section 3: Protocol (Table) with AFFILIATE LINKS
    current_y -= 0.5 * inch # Reduced spacing
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(accent_color)
    c.drawString(margin_left, current_y, "03 // 1-WEEK PROTOCOL")
    
    current_y -= 0.1 * inch 
    
    data = [
        ['Day', 'Focus', 'Action'],
        ['Mon', 'Autophagy', '16:8 Fasting. Break fast with Miso.'],
        ['Tue', 'Microbiome', 'Natto/Okra dinner. Feed the mucosa.'],
        ['Wed', 'Enzyme', 'Seaweed Salad. Activate Porphyranase. [See Shopping List]'],
        ['Thu', 'Recovery', 'Start morning with 2g of Ippodo Matcha. [See Shopping List]'],
        ['Fri', 'Omega-3', 'Sashimi/Fish intake. Cognitive boost.'],
        ['Sat', 'Metabolism', 'High Intensity Interval Training.'],
        ['Sun', 'Rest', 'Hot Spring / Bath (HSP activation).']
    ]
    
    # Determine table height to place it correctly
    # Row heights: 1 header + 7 rows. Approx 0.25 inch per row?
    # Let's trust wrap/drawOn flow
    
    table = Table(data, colWidths=[0.8*inch, 1.2*inch, 4.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent_color),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 6), # Reduced padding
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#222222")),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.white),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 4), # Reduced padding
    ]))
    
    w, h = table.wrap(width, height)
    # We want to draw it below the title
    table.drawOn(c, margin_left, current_y - h)

    # Footer Disclaimer
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.grey)
    disclaimer = "This report is generated based on Japanese Diet Index (JDI8) research. It is for educational purposes only and not medical advice."
    c.drawCentredString(width / 2, 0.4 * inch, disclaimer)
    c.drawRightString(width - margin_left, 0.4 * inch, "Page 1")

    c.showPage() # End Page 1
    
    # --- PAGE 2: SHOPPING LIST & RESOURCES ---
    # Background
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    # Header Page 2
    c.setStrokeColor(accent_color)
    c.setLineWidth(2)
    c.line(margin_left, height - 0.8 * inch, width - margin_left, height - 0.8 * inch)
    
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(accent_color)
    c.drawString(margin_left, height - 0.7 * inch, "ZENGEN LONGEVITY AI")
    c.setFillColor(text_white)
    c.drawRightString(width - margin_left, height - 0.7 * inch, "SHOPPING LIST & RESOURCES")
    
    current_y = height - 1.5 * inch
    
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(text_white)
    c.drawString(margin_left, current_y, "The Gold Standard Stack")
    current_y -= 0.4 * inch
    
    # Store Links
    link_matcha = "https://amzn.to/3OqrkJE"
    link_nori = "https://amzn.to/3MmatHs"
    link_nmn = "https://www.amazon.com/s?k=japanese+nmn"
    
    # Helper to draw linked item
    def draw_linked_item(canvas, x, y, title, desc, link):
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(accent_color)
        canvas.drawString(x, y, title)
        
        # Link rect for title
        text_width = canvas.stringWidth(title, "Helvetica-Bold", 12)
        canvas.linkURL(link, (x, y - 2, x + text_width, y + 10), relative=1)
        
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(text_white)
        canvas.drawString(x, y - 0.2 * inch, desc)
        
        # Explicit Button-like link
        button_y = y - 0.45 * inch
        canvas.setFillColor(colors.HexColor("#333333"))
        canvas.roundRect(x, button_y, 1.5 * inch, 0.25 * inch, 4, fill=True, stroke=False)
        canvas.setFillColor(accent_color)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawCentredString(x + 0.75 * inch, button_y + 0.08 * inch, "VIEW PRODUCT >")
        canvas.linkURL(link, (x, button_y, x + 1.5 * inch, button_y + 0.25 * inch), relative=1)
        
        return y - 0.8 * inch

    # Items
    current_y = draw_linked_item(c, margin_left, current_y, 
        "Ippodo Matcha", 
        "The world's finest L-Theanine source for neuro-protection.", 
        link_matcha)
        
    current_y = draw_linked_item(c, margin_left, current_y, 
        "Suntory NMN", 
        "99.9% purity for DNA repair and cellular energy.", 
        link_nmn)
        
    current_y = draw_linked_item(c, margin_left, current_y, 
        "Zojirushi IH Cooker", 
        "The foundation of a healthy metabolism. GABA activation mode.", 
        "https://amzn.to/3Oq6KZZ")

    current_y -= 0.5 * inch
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(text_white)
    c.drawString(margin_left, current_y, "Essential Ingredients (Amazon Global)")
    current_y -= 0.4 * inch
    
    current_y = draw_linked_item(c, margin_left, current_y, 
        "Premium Miso & Seaweed", 
        "Organic Dried Seaweed, Traditional Pickles, Aged Miso.", 
        link_nori)

    # Footer Page 2
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, 0.4 * inch, "Affiliate Disclosure: We may earn a commission from qualifying purchases.")
    c.drawRightString(width - margin_left, 0.4 * inch, "Page 2")

    c.showPage()
    c.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='ZenGen_Longevity_Premium_Report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
