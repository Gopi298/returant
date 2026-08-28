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

st.title("🩺 Diabetes Prediction System")

st.write(
    "Machine Learning based diabetes risk prediction "
    "using patient clinical information."
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
    max_value=300,
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

# ============================================================
# INFORMATION
# ============================================================

st.divider()

st.info(
    "This application is for educational and research purposes. "
    "It should not be used as a substitute for professional "
    "medical diagnosis."
)
