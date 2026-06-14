
import streamlit as st
import requests
import os

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="SuperKart Sales Prediction Platform",
    layout="centered"
)

# -----------------------------
# API configuration 
# -----------------------------
API_URL = os.getenv(
    "API_URL",
    "https://lasya679-superkartsalesbackend.hf.space/v1/predict"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    .sub-title {
        font-size: 2rem;
        font-weight: 700;
        color: #7c3aed;
    }
    .description {
        font-size: 1.1rem;
        color: #4a5568;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }
    .feature-box {
        text-align: center;
        padding: 0.5rem;
        border-radius: 6px;
    }
    .feature-title {
        font-weight: 600;
        color: #7c3aed;
    }
    .feature-desc {
        color: #555;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #4a5568;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
    <div class="main-header">
        <div class="main-title">Unlock Your Sales Potential 🚀</div>
        <div class="sub-title">SuperKart Predict</div>
        <p class="description">
            AI-powered sales forecasting to optimize inventory and improve business decisions.
        </p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------
# Feature highlights
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-box">
            <div class="feature-title">🧠 Model</div>
            <div class="feature-desc">Random Forest Regressor</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-box">
            <div class="feature-title">⭐ Performance</div>
            <div class="feature-desc">~91% R² Score</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown('<div class="section-title">Enter Product Details</div>', unsafe_allow_html=True)

# -----------------------------
# Input fields
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
    Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.068)
    Product_MRP = st.number_input("Product MRP", min_value=0.0, value=116.7)
    Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])

with col2:
    Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
    Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=17)
    Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])
    Product_Id_char = st.selectbox("Product ID Prefix", ["FD", "NC", "DR"])

st.divider()

# -----------------------------
# Prediction button
# -----------------------------
if st.button("⚡ Run Prediction", use_container_width=True):

    if Product_Weight <= 0:
        st.warning("Invalid Product Weight")
        st.stop()

    if Product_MRP <= 0:
        st.warning("Invalid Product MRP")
        st.stop()

    product_data = {
        "Product_Weight": Product_Weight,
        "Product_Sugar_Content": Product_Sugar_Content,
        "Product_Allocated_Area": Product_Allocated_Area,
        "Product_MRP": Product_MRP,
        "Store_Size": Store_Size,
        "Store_Location_City_Type": Store_Location_City_Type,
        "Store_Type": Store_Type,
        "Store_Age_Years": Store_Age_Years,
        "Product_Type_Category": Product_Type_Category,
        "Product_Id_char": Product_Id_char
    }

    with st.spinner("Generating prediction..."):
        try:
            response = requests.post(
                API_URL,
                json=product_data,
                timeout=10
            )

            response.raise_for_status()
            result = response.json()

            predicted_sales = result.get("predicted_sales")

            if predicted_sales is None:
                st.error("Invalid response from API")
                st.stop()

            st.success("Prediction Successful!")
            st.metric(
                label="Predicted Sales",
                value=f"£{predicted_sales:.2f}"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
