import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Diabetes Prediction AI",
    page_icon="🩺",
    layout="wide"
)

# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("diabetes_model.pkl")


model = load_model()

# ============================================================
# TITLE
# ============================================================

st.title("🩺 Diabetes Prediction & Treatment Guidance System")

st.write(
    "Machine Learning based diabetes risk prediction "
    "using patient clinical information."
)

st.warning(
    "Physician clinical decision-support tool. "
    "Treatment and medication decisions must be confirmed "
    "by a qualified healthcare professional."
)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Patient Information")

pregnancies = st.sidebar.number_input(
    "Pregnancies",
    min_value=0,
    max_value=20,
    value=1,
    step=1
)

glucose = st.sidebar.number_input(
    "Glucose",
    min_value=0,
    max_value=500,
    value=120,
    step=1
)

blood_pressure = st.sidebar.number_input(
    "Blood Pressure",
    min_value=0,
    max_value=200,
    value=70,
    step=1
)

skin_thickness = st.sidebar.number_input(
    "Skin Thickness",
    min_value=0,
    max_value=100,
    value=20,
    step=1
)

insulin = st.sidebar.number_input(
    "Insulin",
    min_value=0,
    max_value=1000,
    value=80,
    step=1
)

bmi = st.sidebar.number_input(
    "BMI",
    min_value=0.0,
    max_value=80.0,
    value=25.0,
    step=0.1
)

diabetes_pedigree = st.sidebar.number_input(
    "Diabetes Pedigree Function",
    min_value=0.0,
    max_value=3.0,
    value=0.5,
    step=0.01
)

age = st.sidebar.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=30,
    step=1
)

# ============================================================
# INPUT DATAFRAME
# ============================================================

input_data = pd.DataFrame({
    "Pregnancies": [pregnancies],
    "Glucose": [glucose],
    "BloodPressure": [blood_pressure],
    "SkinThickness": [skin_thickness],
    "Insulin": [insulin],
    "BMI": [bmi],
    "DiabetesPedigreeFunction": [diabetes_pedigree],
    "Age": [age]
})

# ============================================================
# DISPLAY INPUT
# ============================================================

st.subheader("Patient Details")

st.dataframe(
    input_data,
    use_container_width=True
)

# ============================================================
# PREDICTION BUTTON
# ============================================================

if st.button(
    "🔍 Predict Diabetes",
    use_container_width=True
):

    prediction = model.predict(
        input_data
    )[0]

    probability = model.predict_proba(
        input_data
    )[0][1]

    probability_percent = probability * 100

    st.divider()

    st.subheader("Prediction Result")

    # ========================================================
    # RESULT
    # ========================================================

    if prediction == 1:

        st.error(
            "⚠️ Diabetes Risk Detected"
        )

        st.write(
            f"Predicted diabetes probability: "
            f"**{probability_percent:.2f}%**"
        )

    else:

        st.success(
            "✅ No Diabetes Risk Detected"
        )

        st.write(
            f"Predicted diabetes probability: "
            f"**{probability_percent:.2f}%**"
        )

    # ========================================================
    # PROBABILITY BAR
    # ========================================================

    st.subheader("Prediction Probability")

    st.progress(
        int(probability_percent)
    )

    st.write(
        f"Diabetes probability: "
        f"{probability_percent:.2f}%"
    )

    # ========================================================
    # GLUCOSE LEVEL CLASSIFICATION
    # ========================================================

    st.divider()

    st.subheader("🩸 Glucose Level Assessment")

    if glucose < 70:

        glucose_category = "LOW"

        st.error(
            f"🔴 Low glucose: {glucose} mg/dL"
        )

        st.write(
            "Possible hypoglycemia. Clinical assessment is "
            "recommended, especially when symptoms are present."
        )

    elif glucose < 126:

        glucose_category = "NORMAL / BELOW DIABETES THRESHOLD"

        st.success(
            f"🟢 Glucose level: {glucose} mg/dL"
        )

        st.write(
            "This value is below the diagnostic fasting diabetes "
            "threshold. Interpretation depends on whether the "
            "measurement was fasting or after eating."
        )

    elif glucose < 200:

        glucose_category = "ELEVATED"

        st.warning(
            f"🟡 Elevated glucose: {glucose} mg/dL"
        )

        st.write(
            "Further evaluation with appropriate glucose testing "
            "and/or HbA1c may be required."
        )

    elif glucose < 300:

        glucose_category = "HIGH"

        st.warning(
            f"🟠 High glucose: {glucose} mg/dL"
        )

        st.write(
            "High glucose requires clinical evaluation. "
            "Treatment depends on diabetes type, HbA1c, kidney "
            "function, cardiovascular risk and other factors."
        )

    else:

        glucose_category = "VERY HIGH"

        st.error(
            f"🔴 Very high glucose: {glucose} mg/dL"
        )

        st.write(
            "Very high glucose requires prompt clinical evaluation."
        )

    # ========================================================
    # SIMPLE DIABETES STATUS IMAGE
    # ========================================================

    st.divider()

    st.subheader("🩺 Diabetes Status")

    if prediction == 1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/2966/2966327.png",
            width=120
        )

    else:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/190/190411.png",
            width=120
        )

    # ========================================================
    # TREATMENT GUIDANCE
    # ========================================================

    st.divider()

    st.subheader("💊 Physician Treatment Guidance")

    # ========================================================
    # LOW GLUCOSE
    # ========================================================

    if glucose < 70:

        st.error(
            "🔴 LOW GLUCOSE – HYPOGLYCEMIA ASSESSMENT"
        )

        st.write(
            "Medication should not be automatically increased or "
            "started from this glucose value."
        )

        st.write(
            "Physician should review current insulin and "
            "glucose-lowering medications and evaluate the "
            "cause of hypoglycemia."
        )

        st.write(
            "If the patient is conscious and able to swallow, "
            "follow the established hypoglycemia treatment protocol."
        )

        st.write(
            "🚶 Physical exercise should be avoided until the "
            "low glucose episode has been appropriately addressed."
        )

    # ========================================================
    # BELOW DIABETES THRESHOLD
    # ========================================================

    elif glucose < 126:

        st.success(
            "🟢 NO AUTOMATIC MEDICATION INDICATION FROM THIS VALUE"
        )

        st.write(
            "If diabetes has not been diagnosed, medication is not "
            "automatically indicated from this single glucose value."
        )

        st.write(
            "Physician may consider HbA1c, repeat fasting glucose "
            "and overall diabetes risk."
        )

        st.write(
            "🚶 Lifestyle recommendation: regular walking/physical "
            "activity, healthy diet and weight management when "
            "clinically appropriate."
        )

        if prediction == 0:

            st.info(
                "✅ No diabetes risk predicted by the ML model. "
                "No diabetes medication is automatically recommended "
                "by this application."
            )

    # ========================================================
    # ELEVATED GLUCOSE
    # ========================================================

    elif glucose < 200:

        st.warning(
            "🟡 ELEVATED GLUCOSE – PHYSICIAN REVIEW"
        )

        st.write(
            "Recommended clinical review may include HbA1c, fasting "
            "glucose, repeat testing and assessment of diabetes risk."
        )

        st.write(
            "Possible medication consideration for confirmed "
            "type 2 diabetes:"
        )

        st.write(
            "💊 Metformin – commonly considered as a glucose-lowering "
            "option when clinically appropriate."
        )

        st.write(
            "💊 Other options may include GLP-1 receptor agonist-based "
            "therapy, SGLT2 inhibitors or other glucose-lowering "
            "medications depending on patient characteristics."
        )

        st.info(
            "Dose, tablet strength and morning/evening timing must "
            "be selected by the treating physician after reviewing "
            "HbA1c, renal function, contraindications and current therapy."
        )

        st.write(
            "🚶 Lifestyle: regular walking/physical activity and "
            "appropriate nutrition should be considered."
        )

    # ========================================================
    # HIGH GLUCOSE
    # ========================================================

    elif glucose < 300:

        st.warning(
            "🟠 HIGH GLUCOSE – MEDICAL EVALUATION REQUIRED"
        )

        st.write(
            "Confirmed diabetes should be evaluated with HbA1c and "
            "other relevant clinical information."
        )

        st.write(
            "Possible physician-selected treatment options include:"
        )

        st.write(
            "💊 Metformin – glucose-lowering medication option "
            "when appropriate."
        )

        st.write(
            "💊 GLP-1 receptor agonist-based therapy – may be "
            "considered according to individual patient factors."
        )

        st.write(
            "💊 SGLT2 inhibitor – may be considered when clinically "
            "appropriate, particularly when cardiovascular or kidney "
            "considerations support its use."
        )

        st.write(
            "💊 Other diabetes medications may be selected according "
            "to the patient's clinical condition."
        )

        st.info(
            "Physician must determine the exact drug, strength, "
            "dose and morning/evening administration schedule."
        )

        st.write(
            "🚶 Physical activity should be individualized based "
            "on glucose level, symptoms and clinical condition."
        )

    # ========================================================
    # VERY HIGH GLUCOSE
    # ========================================================

    else:

        st.error(
            "🔴 VERY HIGH GLUCOSE – PROMPT PHYSICIAN EVALUATION"
        )

        st.write(
            f"Current glucose: **{glucose} mg/dL**"
        )

        st.write(
            "Very high glucose requires assessment for symptomatic "
            "hyperglycemia and possible acute metabolic complications."
        )

        st.write(
            "Possible physician treatment considerations may include:"
        )

        st.write(
            "💉 Insulin therapy – may be considered when clinically "
            "indicated. Insulin type, concentration, dose and timing "
            "must be individually prescribed by the physician."
        )

        st.write(
            "💊 Oral/non-insulin glucose-lowering medication may also "
            "be considered depending on diabetes type and clinical status."
        )

        st.error(
            "⚠️ This application does NOT calculate or recommend "
            "an insulin dose in mg or units."
        )

        st.write(
            "🚨 If high glucose is accompanied by vomiting, abdominal "
            "pain, rapid/difficult breathing, confusion, severe "
            "weakness or dehydration, urgent medical evaluation is required."
        )

        st.write(
            "🚶 Do not use exercise as a substitute for medical "
            "evaluation when severe hyperglycemia or acute symptoms "
            "are present."
        )

    # ========================================================
    # PHYSICIAN MEDICATION REVIEW
    # ========================================================

    st.divider()

    st.subheader("👨‍⚕️ Physician Medication Review")

    medication_options = [
        "Metformin",
        "GLP-1 receptor agonist-based therapy",
        "SGLT2 inhibitor",
        "DPP-4 inhibitor",
        "Sulfonylurea",
        "Insulin therapy when clinically indicated"
    ]

    st.write(
        "Potential medication options for physician review:"
    )

    for medication in medication_options:

        st.write(
            f"• {medication}"
        )

    st.info(
        "Medication dose, mg/units, frequency and administration "
        "time should be entered or confirmed by the treating physician. "
        "Glucose level alone is insufficient to safely determine a "
        "patient-specific prescription."
    )

    # ========================================================
    # LIFESTYLE GUIDANCE
    # ========================================================

    st.divider()

    st.subheader("🚶 Lifestyle Guidance")

    st.write(
        "• Regular walking or physical activity when clinically appropriate"
    )

    st.write(
        "• Reduce excess refined carbohydrates and added sugars"
    )

    st.write(
        "• Follow an individualized balanced diet"
    )

    st.write(
        "• Maintain a healthy body weight"
    )

    st.write(
        "• Monitor glucose as advised by the healthcare professional"
    )

    st.write(
        "• Complete recommended HbA1c and follow-up testing"
    )

    # ========================================================
    # MEDICATION DECISION FACTORS
    # ========================================================

    st.divider()

    st.subheader("📋 Physician Decision Factors")

    factors = [
        "HbA1c level",
        "Fasting and post-meal glucose",
        "Diabetes type",
        "Age",
        "Kidney function / eGFR",
        "Heart disease / cardiovascular risk",
        "Weight and obesity status",
        "Risk of hypoglycemia",
        "Current medications",
        "Pregnancy status",
        "Diabetes symptoms",
        "Duration of diabetes"
    ]

    for factor in factors:

        st.write(
            f"• {factor}"
        )

    # ========================================================
    # EMERGENCY WARNING
    # ========================================================

    if glucose >= 300:

        st.divider()

        st.error(
            "🚨 HIGH-RISK WARNING"
        )

        st.write(
            "If very high glucose is accompanied by vomiting, "
            "difficulty breathing, confusion, severe weakness, "
            "dehydration or other severe symptoms, seek urgent "
            "medical care."
        )

# ============================================================
# INFORMATION
# ============================================================

st.divider()

st.info(
    "This application is an educational machine-learning and "
    "physician decision-support project. The model prediction is "
    "not a medical diagnosis and medication guidance is not a "
    "patient-specific prescription."
)
