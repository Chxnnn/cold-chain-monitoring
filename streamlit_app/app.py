import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from utils.snowflake_conn import fetch_data

st.set_page_config(page_title="Cold Chain Dashboard", layout="wide")
st.title("📦 Cold Chain Monitoring Dashboard")
st.caption("Monitor temperatures, detect excursions, and predict risks from Snowflake or CSV.")

# Load ML model
import os
import pickle

# Correct path to model file (relative to streamlit_app/)
import os
import pickle

model_path = os.path.join("model", "risk_model.pkl")
feature_path = os.path.join("model", "feature_columns.pkl")

model = pickle.load(open(model_path, "rb"))
feature_cols = pickle.load(open(feature_path, "rb"))



# Define reusable function for prediction
def predict_risk(df_input):
    df_ml = df_input.copy()
    df_ml["HOUR"] = pd.to_datetime(df_ml["TIMESTAMP"]).dt.hour
    df_ml["WEEKDAY"] = pd.to_datetime(df_ml["TIMESTAMP"]).dt.weekday
    df_ml = pd.get_dummies(df_ml, columns=["LOCATION", "CONTAINER_ID"], dtype=int)
    for col in feature_cols:
        if col not in df_ml:
            df_ml[col] = 0
    df_ml = df_ml[feature_cols]
    df_input["RISK_SCORE"] = model.predict_proba(df_ml)[:, 1]
    return df_input

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 Dashboard (Snowflake)", "📁 Upload CSV"])

# --- Tab 1: Snowflake Dashboard ---
with tab1:
    df = fetch_data()
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])

    # Risk score prediction
    df = predict_risk(df)

    st.success(f"✅ Loaded {len(df)} rows from Snowflake")

    # KPI Tiles
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Avg Temp (°C)", round(df["TEMPERATURE"].mean(), 2))
    col3.metric("Excursions", df[(df["TEMPERATURE"] < 2) | (df["TEMPERATURE"] > 8)].shape[0])

    # Filters
    st.sidebar.header("🔎 Filter Data")
    container = st.sidebar.selectbox("Select Container", ["All"] + sorted(df["CONTAINER_ID"].unique()))
    if container != "All":
        df = df[df["CONTAINER_ID"] == container]

    date_range = st.sidebar.date_input("Select Date Range", [])
    if len(date_range) == 2:
        df = df[(df["TIMESTAMP"] >= pd.to_datetime(date_range[0])) & (df["TIMESTAMP"] <= pd.to_datetime(date_range[1]))]

    # Auto-alerts
    st.subheader("🚨 Auto Alerts: High-Risk Readings")
    high_risk_df = df[df["RISK_SCORE"] > 0.7]
    if high_risk_df.empty:
        st.success("✅ No high-risk excursions detected.")
    else:
        st.error(f"⚠️ {len(high_risk_df)} potential high-risk readings detected!")
        st.dataframe(high_risk_df[["TIMESTAMP", "CONTAINER_ID", "TEMPERATURE", "LOCATION", "RISK_SCORE"]])

    # Charts
    st.subheader("📈 Temperature Over Time")
    fig = px.line(df, x="TIMESTAMP", y="TEMPERATURE", color="CONTAINER_ID", title="Temperature Trends")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Average Temperature by Location")
    loc_df = df.groupby("LOCATION")["TEMPERATURE"].mean().reset_index()
    fig2 = px.bar(loc_df, x="LOCATION", y="TEMPERATURE", title="Average Temp by Location")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📉 Risk Score Distribution")
    fig3 = px.histogram(df, x="RISK_SCORE", nbins=30, title="Risk Score Distribution")
    st.plotly_chart(fig3, use_container_width=True)

    # Raw Data
    st.subheader("📋 Raw Data")
    st.dataframe(df)

# --- Tab 2: Upload CSV + ML Analysis ---
with tab2:
    uploaded_file = st.file_uploader("Upload a cold_chain_data CSV", type="csv")
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        df_upload["TIMESTAMP"] = pd.to_datetime(df_upload["TIMESTAMP"])

        # Risk Score
        df_upload = predict_risk(df_upload)

        # Display KPIs
        st.success("✅ CSV uploaded and processed.")
        col1, col2, col3 = st.columns(3)
        col1.metric("Records", len(df_upload))
        col2.metric("Avg Temp", round(df_upload["TEMPERATURE"].mean(), 2))
        col3.metric("Excursions", df_upload[(df_upload["TEMPERATURE"] < 2) | (df_upload["TEMPERATURE"] > 8)].shape[0])

        # Auto-alerts
        st.subheader("🚨 Auto Alerts from Uploaded Data")
        high_risk_upload = df_upload[df_upload["RISK_SCORE"] > 0.7]
        if high_risk_upload.empty:
            st.success("✅ No high-risk readings detected.")
        else:
            st.error(f"⚠️ {len(high_risk_upload)} high-risk rows detected!")
            st.dataframe(high_risk_upload[["TIMESTAMP", "CONTAINER_ID", "TEMPERATURE", "LOCATION", "RISK_SCORE"]])

        # Chart
        st.subheader("📈 Uploaded Data - Temp over Time")
        fig4 = px.line(df_upload, x="TIMESTAMP", y="TEMPERATURE", color="CONTAINER_ID")
        st.plotly_chart(fig4, use_container_width=True)

        st.subheader("📉 Uploaded Risk Score Distribution")
        fig5 = px.histogram(df_upload, x="RISK_SCORE", nbins=30)
        st.plotly_chart(fig5, use_container_width=True)

        st.subheader("📋 Uploaded CSV Preview")
        st.dataframe(df_upload)
