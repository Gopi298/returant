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
    "This application provides educational clinical guidance only. "
    "It does not prescribe medication or insulin. "
    "Treatment decisions must be made by a qualified healthcare professional."
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
            "This may represent hypoglycemia. "
            "Immediate clinical assessment may be required, "
            "especially if the patient has symptoms."
        )

    elif glucose < 126:

        glucose_category = "NORMAL / BELOW DIABETES THRESHOLD"

        st.success(
            f"🟢 Glucose level: {glucose} mg/dL"
        )

        st.write(
            "This value is below the diagnostic fasting "
            "diabetes threshold. Clinical interpretation "
            "depends on whether the measurement was fasting "
            "or taken after eating."
        )

    elif glucose < 200:

        glucose_category = "ELEVATED"

        st.warning(
            f"🟡 Elevated glucose: {glucose} mg/dL"
        )

        st.write(
            "Further evaluation with appropriate glucose "
            "testing and/or HbA1c may be required."
        )

    elif glucose < 300:

        glucose_category = "HIGH"

        st.warning(
            f"🟠 High glucose: {glucose} mg/dL"
        )

        st.write(
            "High glucose requires clinical evaluation. "
            "Treatment depends on diabetes type, HbA1c, "
            "symptoms, kidney function, cardiovascular "
            "risk and other patient-specific factors."
        )

    else:

        glucose_category = "VERY HIGH"

        st.error(
            f"🔴 Very high glucose: {glucose} mg/dL"
        )

        st.write(
            "Blood glucose ≥300 mg/dL is a level at which "
            "insulin should be considered, particularly "
            "when hyperglycemic symptoms are present. "
            "This requires prompt medical evaluation."
        )

    # ========================================================
    # TREATMENT GUIDANCE
    # ========================================================

    st.divider()

    st.subheader("💊 Treatment Guidance")

    if glucose < 70:

        st.error(
            "Possible hypoglycemia"
        )

        st.write(
            "Do not automatically start diabetes medication "
            "based on this value. The cause of the low glucose "
            "should be evaluated."
        )

        st.write(
            "If the patient is taking insulin or glucose-lowering "
            "medication, a healthcare professional should review "
            "the treatment."
        )

    elif glucose < 126:

        st.success(
            "Lifestyle and monitoring category"
        )

        st.write(
            "Depending on the patient's diagnosis and risk factors, "
            "focus may include healthy nutrition, physical activity, "
            "weight management and regular glucose monitoring."
        )

        st.write(
            "Medication is not automatically indicated from this "
            "single glucose value."
        )

    elif glucose < 200:

        st.warning(
            "Clinical evaluation category"
        )

        st.write(
            "A healthcare professional may evaluate HbA1c, fasting "
            "glucose and other clinical factors before selecting "
            "a treatment plan."
        )

        st.write(
            "For type 2 diabetes, medication selection is individualized."
        )

    elif glucose < 300:

        st.warning(
            "High glucose – medical evaluation recommended"
        )

        st.write(
            "Treatment may involve lifestyle intervention plus "
            "glucose-lowering medication depending on the confirmed "
            "diagnosis and HbA1c."
        )

        st.write(
            "Possible medication classes for type 2 diabetes include "
            "metformin, GLP-1-based therapies, SGLT2 inhibitors and "
            "other glucose-lowering medications. The appropriate "
            "choice depends on the individual patient."
        )

    else:

        st.error(
            "Very high glucose – prompt medical evaluation"
        )

        st.write(
            "Blood glucose ≥300 mg/dL may indicate severe "
            "hyperglycemia."
        )

        st.write(
            "According to ADA 2026 guidance, insulin should be "
            "considered when blood glucose is ≥300 mg/dL or A1C "
            "is >10%, particularly when hyperglycemic symptoms "
            "are present."
        )

        st.write(
            "Do NOT calculate or administer an insulin dose from "
            "this application. Insulin type and dose require "
            "individual clinical assessment."
        )

    # ========================================================
    # DIABETES TYPE / MEDICATION NOTICE
    # ========================================================

    st.divider()

    st.subheader("📋 Medication Decision Factors")

    st.write(
        "A clinician may consider the following before selecting "
        "therapy:"
    )

    factors = [
        "HbA1c level",
        "Fasting and post-meal glucose",
        "Diabetes type",
        "Age",
        "Kidney function",
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
    "This application is an educational machine-learning project. "
    "The model prediction is not a medical diagnosis and the "
    "treatment guidance is not a prescription."
)
