import pandas as pd
import numpy as np
import pickle as pk
import streamlit as st
import base64

# Yerel bir görseli arka plan olarak ekleyen bir fonksiyon
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

# Arka plan görselini ayarla
add_bg_from_local("background/d-render-sports-car-with-lights-goes-camera-black-background_161488-1059.jpg.avif")

# Kaydedilmiş Random Forest modelini yükle
rf_model = pk.load(open('model.pkl', 'rb'))

# Başlık ekle
st.header('Araba Fiyat Tahmin Sistemi')

# Veri setini yükle
cars_data = pd.read_csv('Data_analysis/Processed_Cardetails.csv')

# Marka ve model sütunlarını ayrıştırma
cars_data['brand_name'] = cars_data['name'].apply(lambda x: x.split(' ')[0])  # İlk kelime marka
cars_data['model_name'] = cars_data['name'].apply(lambda x: ' '.join(x.split(' ')[1:]))  # Kalan kısım model

# Kullanıcıdan marka seçimi
brand_selected_name = st.selectbox('Marka Seç', cars_data['brand_name'].unique())

# Seçilen markaya ait modelleri filtreleme
filtered_models = cars_data[cars_data['brand_name'] == brand_selected_name]['model_name'].unique()

# Kullanıcıdan model seçimi
model_selected_name = st.selectbox('Model Seç', filtered_models)

# Kullanıcıdan diğer araç bilgilerini almak için giriş alanları
year = st.slider('Yıl', 1994, 2024)  # Üretim yılı
km_driven = st.number_input('KM', min_value=0, max_value=500000, step=1, format='%d')  # Kullanılmış kilometre

# Türkçe seçenekler
fuel_map = {'Dizel': 'Diesel', 'Benzin': 'Petrol', 'LPG': 'LPG', 'CNG': 'CNG'}
seller_type_map = {'Bireysel': 'Individual', 'Galeri': 'Dealer', 'Güvenilir Galeri': 'Trustmark Dealer'}
transmission_map = {'Manuel': 'Manual', 'Otomatik': 'Automatic'}
owner_map = {
    'İlk Sahibi': 'First Owner', 'İkinci Sahibi': 'Second Owner', 'Üçüncü Sahibi': 'Third Owner',
    'Dördüncü ve Daha Fazla': 'Fourth & Above Owner', 'Test Aracı': 'Test Drive Car'
}

fuel = st.selectbox('Yakıt Tipi', list(fuel_map.keys()))
seller_type = st.selectbox('Satış Tipi', list(seller_type_map.keys()))
transmission = st.selectbox('Vites Türü', list(transmission_map.keys()))
owner = st.selectbox('Araç Durumu', list(owner_map.keys()))
mileage = st.slider('1L Başına Gidilen Kilometre', 10, 40)  # Yakıt verimliliği
engine = st.slider('Motor Hacmi (CC)', 700, 5000)  # Motor hacmi
max_power = st.slider('Motor Gücü (BHP)', 0, 200)  # Motor gücü
seats = st.slider('Koltuk Sayısı', 5, 10)  # Koltuk sayısı

# Kullanıcı tahmin yapmak istediğinde
if st.button("Fiyat Al!"):
    # Seçilen marka ve model isimlerini sayısal değerlere dönüştür
    brand_selected = cars_data[cars_data['brand_name'] == brand_selected_name]['brand'].iloc[0]
    model_selected = cars_data[(cars_data['brand_name'] == brand_selected_name) & 
                                (cars_data['model_name'] == model_selected_name)]['model'].iloc[0]

    # Türkçe seçimleri İngilizceye dönüştür
    fuel_eng = fuel_map[fuel]
    seller_type_eng = seller_type_map[seller_type]
    transmission_eng = transmission_map[transmission]
    owner_eng = owner_map[owner]

    # Model için giriş verilerini oluştur
    input_data_model = pd.DataFrame(
        [[year, km_driven, fuel_eng, seller_type_eng, transmission_eng, owner_eng, mileage, engine, max_power, seats, brand_selected, model_selected]],
        columns=['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats', 'brand', 'model']
    )

    # Kategorik sütunları uygun sayısal değerlere çevir
    input_data_model['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
    input_data_model['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1, 2, 3], inplace=True)
    input_data_model['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)
    input_data_model['owner'].replace(['First Owner', 'Second Owner', 'Third Owner',
                                       'Fourth & Above Owner', 'Test Drive Car'], [1, 2, 3, 4, 5], inplace=True)

    # Random Forest modeliyle tahmin yap
    car_price = rf_model.predict(input_data_model)

    # Tahmini fiyatı optimize et (34 ile çarpılarak Türk lirasına çevrilmiştir.)
    car_price_optimized = abs((int(str(car_price[0]).split('.')[0]) // 100)*34*3)

    # Tahmini fiyatı kullanıcıya göster
    st.markdown(f'Aracınızın Tahmini Fiyatı: **{car_price_optimized} ₺**')
