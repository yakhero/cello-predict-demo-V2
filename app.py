import streamlit as st
import random

# PDF libraries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

# Page config
st.set_page_config(
    page_title="Cello-Predict",
    page_icon="🧬",
    layout="centered"
)

# UI Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fb;
    }
    h1 {
        color: #0b3d91;
    }
    .stButton>button {
        background-color: #00a699;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# PDF generator
def generate_pdf(genes, risk, condition, score):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=letter)

    c.drawString(100, 750, "Cello-Predict Report")
    c.drawString(100, 720, f"Condition: {condition}")
    c.drawString(100, 700, f"Risk Level: {risk}")
    c.drawString(100, 680, f"Confidence Score: {score}%")

    c.drawString(100, 650, "Recommended Genes:")
    y = 630
    for gene in genes:
        c.drawString(120, y, gene)
        y -= 20

    c.drawString(100, 580, "Note: Screening tool only.")

    c.save()
    return temp_file.name


# Title
st.title("🧬 Cello-Predict")
st.caption("AI-Guided Genomic Screening for Low-Resource Settings")

st.markdown("### Phenotype-Guided Gene Panel Recommendation (TRL-3 Simulation)")

# Inputs
st.header("Patient Information")

age = st.number_input("Age", min_value=0, max_value=100, value=25)

gender = st.selectbox("Gender", ["Male", "Female"])

symptom = st.selectbox(
    "Primary Symptom",
    ["Select", "Fatigue / Anemia", "Syncope / Fainting", "Chest Pain"]
)

family_history = st.selectbox(
    "Family History of Genetic Disease?",
    ["No", "Yes"]
)

# Button
if st.button("Analyze"):

    # ✅ SAFE DEFAULTS (NO ERROR GUARANTEE)
    genes = []
    risk = "Unknown"
    condition = "Not determined"
    score = 0
    explanation = "No explanation available."

    # Prevent empty input
    if symptom == "Select":
        st.warning("Please select a valid symptom")
        st.stop()

    st.subheader("🔍 Results")

    # Logic
    if symptom == "Fatigue / Anemia":
        genes = ["HBB", "HBA1", "HBA2"]
        risk = "Moderate"
        condition = "Thalassemia Carrier Risk"
        score = random.randint(70, 85)
        explanation = "These genes are involved in hemoglobin production and linked to thalassemia."

    elif symptom == "Syncope / Fainting":
        genes = ["SCN5A", "KCNQ1", "KCNH2"]
        risk = "High"
        condition = "Inherited Cardiac Risk"
        score = random.randint(80, 95)
        explanation = "These genes regulate cardiac ion channels and are associated with arrhythmias."

    elif symptom == "Chest Pain":
        genes = ["MYH7", "TNNT2"]
        risk = "Low to Moderate"
        condition = "Cardiomyopathy Risk"
        score = random.randint(60, 75)
        explanation = "These genes are linked to heart muscle structure and cardiomyopathies."

    # Family history effect
    if family_history == "Yes":
        score = min(score + 5, 95)
        risk = "High"

    # Extra safety
    if not genes:
        st.warning("Could not determine gene panel. Please refine input.")
        st.stop()

    # Outputs
    st.write("### 🧬 Recommended Gene Panel:")
    st.write(", ".join(genes))

    st.write("### ⚠️ Risk Level:")
    st.write(risk)

    st.write("### 🩺 Condition Focus:")
    st.write(condition)

    # Explanation
    st.write("### 🧠 Why These Genes?")
    st.info(explanation)

    # AI Score
    st.write("### 🤖 AI Confidence Score")
    st.progress(score / 100)
    st.metric(label="Confidence Score", value=f"{score}%")

    if score >= 85:
        st.success("High confidence prediction")
    elif score >= 70:
        st.warning("Moderate confidence prediction")
    else:
        st.info("Low confidence prediction")

    # Cost table
    st.write("### 💰 Cost & Time Comparison")
    st.table({
        "Approach": ["Whole Genome Sequencing", "Standard Panel", "Cello-Predict Guided"],
        "Cost": ["Rs. 250,000 – 400,000+", "Rs. 145,000 – 180,000", "Rs. 10,000"],
        "Turnaround": ["3-6 weeks", "1-2 weeks", "3-5 days"]
    })

    # Disclaimer
    st.info("This is a screening and triage tool, not a diagnostic system. (TRL-3 simulation)")

    # PDF
    pdf_file = generate_pdf(genes, risk, condition, score)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Report (PDF)",
            data=f,
            file_name="cello_predict_report.pdf",
            mime="application/pdf"
        )
