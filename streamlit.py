import streamlit as st
import pickle
import mlflow.pyfunc
import pandas as pd
st.set_page_config(page_title="Stock Price Prediction", layout="wide")

with open("C:/Users/Sagana/Desktop/FAANG_Project/encoded_data.pkl", "rb") as f:
    df_encoded = pickle.load(f)

with open("C:/Users/Sagana/Desktop/FAANG_Project/feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

st.title("📈 Stock Price Prediction App")

# st.markdown("<h1 style='text-align: left;'>Set the stock parameters</h1>", unsafe_allow_html=True)
import streamlit as st


mlflow.set_tracking_uri("http://127.0.0.1:5000")

model_name = "XGB"  
model_uri = f"models:/{model_name}/3"  
model = mlflow.pyfunc.load_model(model_uri)

st.sidebar.header("Company & Price Inputs")
# st.sidebar.markdown("<h3 style='color: maroon;'>Company</h3>", unsafe_allow_html=True)
company = st.sidebar.radio("Company",options=["Amazon", "Apple", "Facebook", "Google", "Netflix"])

company_columns = {
    "Amazon": "Company_Amazon",
    "Apple": "Company_Apple",
    "Facebook": "Company_Facebook",
    "Google": "Company_Google",
    "Netflix": "Company_Netflix"
}


# st.sidebar.markdown("<h3 style='color: White;'>Opening price</h3>", unsafe_allow_html=True)
open_price = st.sidebar.slider("Open price", 1, 500, 1000, key="open_price_slider")

# st.sidebar.markdown("<h3 style='color: maroon;'>Low price</h3>", unsafe_allow_html=True)
Low_price = st.sidebar.slider("Low price", 1,500, 1000, key="low_price_slider")

# st.sidebar.markdown("<h3 style='color: maroon;'>High price</h3>", unsafe_allow_html=True)
High_price = st.sidebar.slider("High price", 1,100, 1000, key="high_price_slider")

# st.sidebar.markdown("<h3 style='color: maroon;'>Volume</h3>", unsafe_allow_html=True)
vol= st.sidebar.number_input("Volume", min_value=10000, max_value=500000)

from datetime import date

selected_date = st.sidebar.date_input("📅 Select Date", value=date(2025, 1, 1))
year, month, day = selected_date.year, selected_date.month, selected_date.day

input_data = {}

for col in feature_columns:  
    
    if col== 'Open':
        input_data[col] =open_price
    elif col== 'High':
        input_data[col] =High_price
    elif col== 'Low':
        input_data[col] =Low_price
    elif col== 'Volume':
        input_data[col] =vol
    elif col == 'Analyst Recommendation':
        analyst_mapping = {"Buy": 1, "Sell": 0}
        options = ["Select"] + list(analyst_mapping.keys())
        analyst_choice = st.selectbox(f"{col}", options, index=0)
        if analyst_choice == "Select":
            input_data[col] = 0  
        else:
            input_data[col] = analyst_mapping[analyst_choice]


    elif col in ["Year", "Month", "Day"]:
        input_data["Year"]=year
        input_data["Month"]=month
        input_data["Day"]=day
    elif col in ["Company_Amazon", "Company_Apple", "Company_Facebook", "Company_Google", "Company_Netflix"]:
        for com in ["Company_Amazon", "Company_Apple", "Company_Facebook", "Company_Google", "Company_Netflix"]:
            if col== company:
                input_data[col] =1
            else:
                input_data[col] =0
    else:
        options = ["Select"] + list(df_encoded[col].unique())
        selected_value = st.selectbox(f"{col}", options, index=0)
        if selected_value != "Select":
            input_data[col] = selected_value
        else:
            input_data[col] = None 

input_df = pd.DataFrame([input_data])

if st.button("Predict Stock Price"):
    prediction = model.predict(input_df)
    st.success(f"Predicted Close Price: {prediction[0]:.2f}")
