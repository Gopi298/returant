"""
==========================================================================
 DIABETES RISK PREDICTOR - Streamlit App
 Loads the pre-trained model (models/best_model.pkl) and scaler to
 predict diabetes risk from user input. Ready for Streamlit Cloud.
==========================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# LOAD MODEL, SCALER, METADATA  (cached so it only loads once)
# --------------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("models/best_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    with open("models/metadata.json") as f:
        metadata = json.load(f)
    return model, scaler, metadata

model, scaler, metadata = load_artifacts()
FEATURES = metadata["feature_names"]

# --------------------------------------------------------------------------
# STYLES
# --------------------------------------------------------------------------
st.markdown("""
<style>
    .main-header {font-size: 2.3rem; font-weight: 700; color: #1f4e79; margin-bottom: 0;}
    .sub-header {color: #666; font-size: 1.05rem; margin-top: 0;}
    .metric-card {background-color: #f0f4f8; padding: 1rem; border-radius: 10px; text-align:center;}
    .risk-high {background-color: #ffe3e3; padding: 1.2rem; border-radius: 10px; border-left: 6px solid #c0392b;}
    .risk-low  {background-color: #e3f9e5; padding: 1.2rem; border-radius: 10px; border-left: 6px solid #27ae60;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# SIDEBAR - PATIENT INPUT
# --------------------------------------------------------------------------
st.sidebar.header("🧾 Patient Data Input")
st.sidebar.caption("Adjust the sliders to match the patient's measurements.")

def user_input_form():
    pregnancies = st.sidebar.slider("Pregnancies", 0, 17, 2)
    glucose = st.sidebar.slider("Glucose (mg/dL)", 40, 200, 117)
    blood_pressure = st.sidebar.slider("Blood Pressure (mm Hg)", 24, 130, 72)
    skin_thickness = st.sidebar.slider("Skin Thickness (mm)", 7, 99, 23)
    insulin = st.sidebar.slider("Insulin (mu U/ml)", 14, 850, 100)
    bmi = st.sidebar.slider("BMI", 15.0, 67.0, 32.0, step=0.1)
    dpf = st.sidebar.slider("Diabetes Pedigree Function", 0.05, 2.5, 0.37, step=0.01)
    age = st.sidebar.slider("Age", 18, 90, 30)

    data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": dpf,
        "Age": age,
    }
    return pd.DataFrame([data])[FEATURES]

input_df = user_input_form()

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.markdown('<p class="main-header">🩺 Diabetes Risk Predictor</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="sub-header">Powered by a tuned <b>{metadata["model_name"]}</b> model '
    f'&nbsp;|&nbsp; Test Accuracy: <b>{metadata["test_accuracy"]*100:.1f}%</b> '
    f'&nbsp;|&nbsp; ROC AUC: <b>{metadata["roc_auc"]:.3f}</b></p>',
    unsafe_allow_html=True,
)
st.divider()

tab1, tab2, tab3 = st.tabs(["🔮 Prediction", "📊 Patient Data", "📈 Model Info"])

# --------------------------------------------------------------------------
# TAB 1: PREDICTION
# --------------------------------------------------------------------------
with tab1:
    col1, col2 = st.columns([1, 1.3])

    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    proba = model.predict_proba(input_scaled)[0]
    risk_pct = proba[1] * 100

    with col1:
        st.subheader("Result")
        if prediction == 1:
            st.markdown(
                f'<div class="risk-high"><h3>⚠️ High Risk of Diabetes</h3>'
                f'<p>Estimated probability: <b>{risk_pct:.1f}%</b></p></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="risk-low"><h3>✅ Low Risk of Diabetes</h3>'
                f'<p>Estimated probability: <b>{risk_pct:.1f}%</b></p></div>',
                unsafe_allow_html=True,
            )

        st.caption(
            "⚠️ This tool is for educational purposes only and is **not** a medical "
            "diagnosis. Please consult a healthcare professional for medical advice."
        )

    with col2:
        # Gauge chart for probability
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            title={"text": "Diabetes Risk (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1f4e79"},
                "steps": [
                    {"range": [0, 30], "color": "#d4f4dd"},
                    {"range": [30, 60], "color": "#fff3cd"},
                    {"range": [60, 100], "color": "#f8d7da"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "value": 50},
            },
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Input Summary")
    st.dataframe(input_df.style.format(precision=2), use_container_width=True)

# --------------------------------------------------------------------------
# TAB 2: PATIENT DATA VISUALS (compare patient vs population)
# --------------------------------------------------------------------------
with tab2:
    st.subheader("How does this patient compare to the training population?")
    ranges = metadata["feature_ranges"]

    cols = st.columns(4)
    for i, feat in enumerate(FEATURES):
        lo, hi = ranges[feat]
        val = input_df[feat].values[0]
        pct = (val - lo) / (hi - lo) * 100 if hi > lo else 50
        with cols[i % 4]:
            st.metric(feat, f"{val:.1f}")
            st.progress(min(max(pct / 100, 0), 1.0))

# --------------------------------------------------------------------------
# TAB 3: MODEL INFO
# --------------------------------------------------------------------------
with tab3:
    st.subheader("Model Performance")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Model", metadata["model_name"])
    c2.metric("Test Accuracy", f"{metadata['test_accuracy']*100:.1f}%")
    c3.metric("CV Accuracy", f"{metadata['cv_accuracy_mean']*100:.1f}%")
    c4.metric("ROC AUC", f"{metadata['roc_auc']:.3f}")

    st.info(
        f"**Overfitting check:** Train/Test accuracy gap = "
        f"**{metadata['overfit_gap']*100:.1f} points** "
        f"({'looks healthy ✅' if metadata['overfit_gap'] < 0.10 else 'watch for overfitting ⚠️'})"
    )

    st.caption(
        "This model was trained and selected from 7-8 candidate algorithms "
        "(Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, "
        "SVM, KNN, Naive Bayes, XGBoost) using 5-fold cross-validation, with the "
        "final choice balancing accuracy and overfit gap, then hyperparameter-tuned."
    )

    if hasattr(model, "feature_importances_"):
        st.subheader("Feature Importance")
        imp_df = pd.DataFrame({
            "Feature": FEATURES,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=True)
        fig2 = go.Figure(go.Bar(
            x=imp_df["Importance"], y=imp_df["Feature"], orientation="h",
            marker_color="#1f4e79"
        ))
        fig2.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.caption("Built with Streamlit · scikit-learn · Random Forest classifier trained on the Pima Indians Diabetes dataset.")
