import os
import streamlit as st
import pandas as pd
from tabpfn_client import TabPFNRegressor
from sklearn.model_selection import train_test_split

os.environ["TABPFN_API_TOKEN"] = "tabpfn_sk_D7KGDgEsuT4FSCME7Mzy1vkot7F46YOkStUUyc3xhns"

@st.cache_resource
def train_model():
    os.environ["TABPFN_API_TOKEN"] = "tabpfn_sk_D7KGDgEsuT4FSCME7Mzy1vkot7F46YOkStUUyc3xhns"
    df = pd.read_excel("SAND.xlsx")
    target_col = "Gmax (MPa)"
    df.dropna(subset=[target_col], inplace=True)
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model = TabPFNRegressor()  # ← removed random_state
    model.fit(X_train, y_train)
    return model

st.title("TabPFN — Gmax (MPa) Prediction")
st.write("Enter soil parameters to predict maximum shear modulus:")

with st.spinner("Training model on first run, please wait..."):
    model = train_model()

st.success("Model ready.")

D50_mm     = st.number_input("D50 (mm)",  value=0.619, format="%.3f")
Cu         = st.number_input("Cu",        value=1.46,  format="%.2f")
emax       = st.number_input("emax",      value=0.742, format="%.3f")
emin       = st.number_input("emin",      value=0.502, format="%.3f")
sigma3_kPa = st.number_input("σ3'(kPa)", value=50.0,  format="%.1f")
e_c        = st.number_input("e_c",       value=0.665, format="%.3f")

if st.button("Predict Gmax"):
    os.environ["TABPFN_API_TOKEN"] = "tabpfn_sk_D7KGDgEsuT4FSCME7Mzy1vkot7F46YOkStUUyc3xhns"
    input_data = pd.DataFrame([{
        "D50 (mm)":  D50_mm,
        "Cu":        Cu,
        "emax":      emax,
        "emin":      emin,
        "σ3'(kPa)": sigma3_kPa,
        "e_c":       e_c
    }])
    try:
        prediction = model.predict(input_data)
        st.success(f"Predicted Gmax: **{prediction[0]:.2f} MPa**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
