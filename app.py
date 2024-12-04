import pandas as pd
import numpy as np
import pickle as pk
import streamlit as st
import base64
import shap

# Function to add a background image
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/avif;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Allow the user to upload a custom background image
bg_image_path = st.file_uploader("Upload Background Image", type=["jpg", "png", "avif"])
if bg_image_path is not None:
    add_bg_from_local(bg_image_path)
else:
    add_bg_from_local("background/d-render-sports-car-with-lights-goes-camera-black-background_161488-1059.jpg.avif")

# Load the Random Forest model
with st.spinner('Loading model...'):
    rf_model = pk.load(open('model.pkl', 'rb'))

# Title
st.header('Car Price Prediction System')

# Load dataset
cars_data = pd.read_csv('Data_analysis/Processed_Cardetails.csv')

# Split brand and model from the name column
cars_data['brand_name'] = cars_data['name'].apply(lambda x: x.split(' ')[0])
cars_data['model_name'] = cars_data['name'].apply(lambda x: ' '.join(x.split(' ')[1:]))

# User input for brand and model selection
brand_selected_name = st.selectbox('Select Brand', cars_data['brand_name'].unique())
filtered_models = cars_data[cars_data['brand_name'] == brand_selected_name]['model_name'].unique()
model_selected_name = st.selectbox('Select Model', filtered_models)

# Input fields for other car attributes
year = st.slider('Year', 1994, 2024)
km_driven = st.number_input('Kilometers Driven', min_value=0, max_value=500000, step=1, format='%d')

# Mappings for localized options
fuel_map = {'Diesel': 'Diesel', 'Petrol': 'Petrol', 'LPG': 'LPG', 'CNG': 'CNG'}
seller_type_map = {'Individual': 'Individual', 'Dealer': 'Dealer', 'Trustmark Dealer': 'Trustmark Dealer'}
transmission_map = {'Manual': 'Manual', 'Automatic': 'Automatic'}
owner_map = {
    'First Owner': 'First Owner', 'Second Owner': 'Second Owner',
    'Third Owner': 'Third Owner', 'Fourth & Above Owner': 'Fourth & Above Owner', 'Test Drive Car': 'Test Drive Car'
}

fuel = st.selectbox('Fuel Type', list(fuel_map.keys()))
seller_type = st.selectbox('Seller Type', list(seller_type_map.keys()))
transmission = st.selectbox('Transmission Type', list(transmission_map.keys()))
owner = st.selectbox('Owner Status', list(owner_map.keys()))
mileage = st.slider('Mileage (km/L)', 10, 40)
engine = st.slider('Engine Size (CC)', 700, 5000)
max_power = st.slider('Max Power (BHP)', 0, 200)
seats = st.slider('Number of Seats', 5, 10)

# Prediction logic
if st.button("Predict Price"):
    try:
        # Process inputs
        brand_selected = cars_data[cars_data['brand_name'] == brand_selected_name]['brand'].iloc[0]
        model_selected = cars_data[(cars_data['brand_name'] == brand_selected_name) &
                                    (cars_data['model_name'] == model_selected_name)]['model'].iloc[0]

        # Create input DataFrame
        input_data_model = pd.DataFrame(
            [[year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, seats, brand_selected, model_selected]],
            columns=['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats', 'brand', 'model']
        )

        # Encode categorical features
        encode_column(input_data_model, 'fuel', fuel_map)
        encode_column(input_data_model, 'seller_type', seller_type_map)
        encode_column(input_data_model, 'transmission', transmission_map)
        encode_column(input_data_model, 'owner', owner_map)

        # Make prediction
        car_price = rf_model.predict(input_data_model)
        confidence_interval = (car_price[0] * 0.95, car_price[0] * 1.05)

        # Display result
        st.success(f"Estimated Price: {int(car_price[0])} ₺")
        st.info(f"Confidence Interval: {int(confidence_interval[0])} ₺ - {int(confidence_interval[1])} ₺")

        # Explain prediction with SHAP
        explainer = shap.TreeExplainer(rf_model)
        shap_values = explainer.shap_values(input_data_model)
        st.pyplot(shap.summary_plot(shap_values, input_data_model))

    except Exception as e:
        st.error(f"Error: {e}")
