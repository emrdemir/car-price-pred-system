
# Araba Fiyat Tahmin Sistemi

Bu proje, kullanıcıdan alınan araç bilgilerine göre araç fiyat tahmini yapan bir Streamlit uygulamasıdır.

## Özellikler

- Kullanıcıdan araç özelliklerini (marka, yıl, kilometre, yakıt tipi, vites türü vb.) alır.
- Model tahminiyle aracın fiyatını hesaplar.
- Arka plan görseli ve Türkçe seçeneklerle kullanıcı dostu bir arayüz sağlar.

---

## Gereklilikler

Bu projeyi çalıştırmadan önce aşağıdaki adımları takip edin:

1. **Python Kurulumu**  
   Proje, Python 3.8+ sürümünde çalışacak şekilde tasarlanmıştır. Python'u sisteminize kurun.

2. **Gerekli Kütüphaneler**  
   Aşağıdaki kütüphaneler gereklidir:
   - `pandas`
   - `numpy`
   - `pickle`
   - `streamlit`

   Gerekli kütüphaneleri yüklemek için aşağıdaki komutu çalıştırabilirsiniz:
   ```bash
   pip install -r requirements.txt
   ```

3. **Model Dosyası (`model.pkl`) ve Veri Seti (`Cardetails.csv`)**  
   - `model.pkl`: Eğitilmiş model dosyasını proje dizinine yerleştirin.
   - `Cardetails.csv`: Araç bilgilerini içeren CSV dosyasını proje dizinine ekleyin.

4. **Arka Plan Görseli**  
   Bir arka plan görseli eklemek isterseniz, uygun bir `.avif` formatında görseli belirttiğiniz dizine koyabilirsiniz.

---

## Kurulum ve Çalıştırma

Aşağıdaki adımları takip ederek projeyi çalıştırabilirsiniz:

1. **Depoyu Klonlayın veya İndirin**  
   Proje dosyalarını bilgisayarınıza alın.

2. **Gerekli Kütüphaneleri Yükleyin**  
   Terminalde aşağıdaki komutu çalıştırarak gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. **Streamlit Uygulamasını Başlatın**  
   Terminalde şu komutu çalıştırın:
   ```bash
   streamlit run app.py
   ```

4. **Web Arayüzüne Erişim**  
   Komut çalıştıktan sonra bir bağlantı göreceksiniz (ör. `http://localhost:8501`). Bu bağlantıyı bir tarayıcıda açarak uygulamayı kullanabilirsiniz.

---

## Dosya Yapısı

- `app.py`: Streamlit uygulaması için ana dosya.
- `model.pkl`: Eğitilmiş model dosyası.
- `Cardetails.csv`: Araç bilgilerini içeren veri seti.
- `requirements.txt`: Gerekli Python kütüphanelerini içeren dosya.
- `README.md`: Proje hakkında bilgi veren dosya.

---
