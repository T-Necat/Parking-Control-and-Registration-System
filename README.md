
# Yapay Zeka Destekli Otopark Yönetim Sistemi

## Proje Tanımı
Bu proje, yapay zeka ve veritabanı teknolojilerini birleştirerek otopark yönetimini kolaylaştırmayı amaçlayan bir sistem sunar. Otoparka giren araçların plakalarını, tiplerini ve üretilecek ücretlerini kaydeden, hem manuel hem de yapay zeka destekli veri girişi sağlayan bir platformdur.

## Özellikler
- **Yapay Zeka Entegrasyonu**: Güvenlik kamerasından elde edilen görüntüler yardımıyla araç tespiti, plaka okuma ve araç tipi sınıflandırması.
- **Manuel Veri Girişi**: Kullanıcılar tarafından plaka, araç tipi ve kalış sürelerini elle girme imkânı.
- **Zaman ve Fiyat Hesaplama**: Araçların otoparkta kaldığı süreye ve araç tipine göre otomatik ücretlendirme.
- **Veritabanı Yönetimi**: Tüm bilgiler PostgreSQL tabanlı bir veritabanında saklanır.

## Veritabanı Yapısı
- **roles**: Kullanıcı rollerini saklar (rol adı ve açıklama).
- **users**: Kullanıcı bilgilerini ve rolleri saklar.
- **vehicle_type**: Araç tiplerini ve bunlara ait fiyat bilgilerini saklar.
- **vehicles**: Araçların plaka numaralarını, tiplerini ve tespit durumunu saklar.
- **parking_records**: Otopark kayıtları (giriş çıkış saatleri, maliyet ve kullanıcı bilgileri).
- **system_info**: Sistemle ilgili genel bilgileri saklar (son bitirme kaydı gibi).

## Kullanım
Projeyi çalıştırmak için aşağıdaki adımları izleyin:

1. **Bağımlılıkları Yükleyin**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Veritabanını Oluşturun**:
   ```bash
   python create_database.py
   ```

3. **Uygulamayı Başlatın**:
   ```bash
   python main.py
   ```

## Dosya Yapısı
- **create_database.py**: Veritabanı tablolarını oluşturur.
- **main.py**: Yapay zeka modelini çalıştırır ve veritabanı ile etkileşir.
- **requirements.txt**: Projede kullanılan Python kütüphanelerini listeler.

## Yapay Zeka Sistemi
Sistemde kullanılan yapay zeka modeli, güvenlik kamerasından gelen verileri işler ve aşağıdaki bilgileri tespit eder:
- Araç plaka numarası
- Araç tipi (binek, ticari vb.)
- Araç tespit durumu (is_detected)

Bu bilgiler, sistem tarafından otomatik olarak veritabanına kaydedilir ve ilgili fiyat şeması ile ücretlendirilir.

## Katkıda Bulunma
Bu projeye katkıda bulunmak isterseniz, bir **pull request** gönderebilirsiniz.

## Lisans
Bu proje MIT Lisansı ile lisanslanmıştır.

---

Bu README dosyası, projenin yapısını ve özelliklerini detaylı bir şekilde açıklamak için hazırlanmıştır. Daha fazla bilgi için geliştiricilerle iletişime geçebilirsiniz.
