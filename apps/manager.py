import streamlit as st
import pandas as pd
import main_page 
import subprocess, os, signal, re



def show_manager_page():
    st.set_page_config(page_title="Manager Sayfası", layout="wide")
    
    # Veritabanı bağlantısını alın
    conn = main_page.get_db_connection()
    cur = conn.cursor()
    
    user_id = st.session_state.user_id
    
    st.title("Manager Sayfası")
    st.success(f"Hoş geldiniz!")
    
    # İki sütun oluştur
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Araç Listesi")
        try:
            tab1, tab2, tab3 = st.tabs(["Tüm Araçlar", "Manuel Eklenler", "Model Tespiti"])
            
            with tab1:
                cur.execute("""
                    SELECT v.plate_number, t.type_name, v.is_detected
                    FROM vehicles v
                    JOIN vehicle_type t ON v.type_id = t.type_id
                """)
                vehicles_data = cur.fetchall()

                # Bir pandas dataframe'e dönüştürelim
                vehicles_df = pd.DataFrame(vehicles_data, columns=["Plaka", "Tip", "Model Tespiti?"])
                st.dataframe(vehicles_df, use_container_width=True)
            
            with tab2:
                cur.execute("""
                    SELECT v.plate_number, t.type_name, v.is_detected
                    FROM vehicles v
                    JOIN vehicle_type t ON v.type_id = t.type_id
                    WHERE v.is_detected = false;
                """)
                vehicles_data = cur.fetchall()

                # Bir pandas dataframe'e dönüştürelim
                vehicles_df = pd.DataFrame(vehicles_data, columns=["Plaka", "Tip", "Model Tespiti?"])
                st.dataframe(vehicles_df, use_container_width=True)
            
            with tab3:
                cur.execute("""
                    SELECT v.plate_number, t.type_name, v.is_detected
                    FROM vehicles v
                    JOIN vehicle_type t ON v.type_id = t.type_id
                    WHERE v.is_detected = true;
                """)
                vehicles_data = cur.fetchall()

                # Bir pandas dataframe'e dönüştürelim
                vehicles_df = pd.DataFrame(vehicles_data, columns=["Plaka", "Tip", "Model Tespiti?"])
                st.dataframe(vehicles_df, use_container_width=True)
            

        except Exception as e:
            st.error(f"Araçlar listelenirken hata oluştu: {e}")

    with col2:
        st.subheader("Kazanç Detayları")
        try:
            # Kazanç detaylarını View'den çekiyoruz
            cur.execute("SELECT * FROM vehicle_income_view;")
            income_data = cur.fetchall()
            income_df = pd.DataFrame(income_data, columns=["Araç Tipi", "Araç Sayısı", "Toplam Kazanç"])
            
            # Tüm kazançların toplamını hesapla
            total_income = income_df["Toplam Kazanç"].sum()
            st.write(f"**Kazanç:** {total_income:.2f} ₺")
            
            st.dataframe(income_df, use_container_width=True, hide_index=True)


        except Exception as e:
            st.error(f"Kazanç detayları yüklenirken hata oluştu: {e}")
            
    st.divider()
    
    st.write("Otoparktan elde edilen toplam kazancı ve bu kazanca hangi kayıtların dahil olduğunu görmek için butona basınız.")

    if st.button("Toplam Kazancı ve Kayıtları Göster"):
        try:
            # Toplam kazanç bilgisi
            cur.execute("SELECT total_earnings FROM total_earnings_view;")
            result = cur.fetchone()
            
            if result and result[0] is not None:
                total_earnings = result[0]
                st.info(f"Toplam kazanç: {total_earnings} ₺")
            else:
                st.warning("Henüz kazanç kaydı bulunamadı.")

            # last_end_day_id değerini al
            cur.execute("SELECT last_end_day_id FROM system_info WHERE id = 1;")
            last_end_day_id = cur.fetchone()[0]

            # Sadece last_end_day_id'den sonra eklenen kayıtları göster
            cur.execute("""
                SELECT record_id, plate_number, entry_time, cost 
                FROM parking_records 
                WHERE cost IS NOT NULL AND record_id > %s;
            """, (last_end_day_id,))
            detailed_records = cur.fetchall()

            if detailed_records:
                df = pd.DataFrame(detailed_records, columns=["Record ID", "Plate Number", "Entry Time", "Cost"])
                st.write("**Kazanca dahil olan kayıtlar:**")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Kazanca dahil edilebilecek herhangi bir yeni kayıt bulunamadı.")
        
        except Exception as e:
            st.error(f"Veri alınırken hata oluştu: {e}")
            
        
    if st.button("Gün Sonu İşlemini Başlat"):
            try:
                cur.execute("CALL end_day_ops();")
                conn.commit()
                st.success("Gün sonu işlemi başarıyla tamamlandı!")
            except Exception as e:
                conn.rollback()
                st.error(f"Gün sonu işlemi yapılırken hata oluştu: {e}")    
    
    st.divider()

    
    col5, col6 = st.columns(2)
    
    # Araç tiplerini veritabanından çek
    cur.execute("SELECT type_id, type_name FROM vehicle_type;")
    types = cur.fetchall()  # [(1, 'Car'), (2, 'Motorcycle'), ...]
    
    # Araç tiplerinin ad listesi
    type_names = [t[1] for t in types]
    
    with col5:
        st.write("#### Araç Ekle")
        plate_input = st.text_input("Plaka giriniz:")
        selected_type_name = st.selectbox("Araç tipi seçiniz:", type_names, None)

        if st.button("Aracı Kaydet"):
            if plate_input.strip() == "":
                st.error("Plaka alanı boş olamaz!")
                
            elif selected_type_name is None:
                st.error("Lütfen bir araç tipi seçiniz!")
                
            elif not re.fullmatch(r'^[A-Z0-9 ]+$', plate_input.upper()):
                st.error("Plaka yalnızca harfler ve rakamlardan oluşmalıdır (örn: '34ABC123').")
                
            else:
                # Seçilen araç tipine ait type_id'yi bul
                selected_type_id = None
                for t_id, t_name in types:
                    if t_name == selected_type_name:
                        selected_type_id = t_id
                        break
                
                try:
                    # Plaka kontrolü
                    check_query = "SELECT COUNT(*) FROM vehicles WHERE plate_number = %s;"
                    cur.execute(check_query, (plate_input,))
                    exists = cur.fetchone()[0]

                    if exists > 0:
                        st.error(f"{plate_input} plakalı araç zaten sistemde mevcut!")
                    else:
                        # Araç tipine ait fiyatı al
                        price_query = "SELECT price FROM vehicle_type WHERE type_id = %s;"
                        cur.execute(price_query, (selected_type_id,))
                        result = cur.fetchone()

                        if not result:
                            st.error("Seçilen araç tipine ait fiyat bilgisi bulunamadı!")
                        else:
                            vehicle_price = result[0]

                            # Araç ve kayıt ekleme
                            insert_vehicle_query = "INSERT INTO vehicles (plate_number, type_id, is_detected) VALUES (%s, %s, %s);"
                            cur.execute(insert_vehicle_query, (plate_input, selected_type_id, False))

                            insert_record_query = "INSERT INTO parking_records (plate_number, entry_time, cost, user_id) VALUES (%s, NOW(), %s, %s);"
                            cur.execute(insert_record_query, (plate_input, vehicle_price, user_id))

                            conn.commit()
                            st.success(f"{plate_input} plakalı araç başarıyla eklendi!")
                except Exception as e:
                    conn.rollback()
                    st.error(f"Araç eklenirken hata oluştu: {e}")
                    
    
    with col6:
        st.write("### Araç Silme İşlemi")
        try:
            
            try:
                # Vehicles tablosundaki bilgileri çekiyoruz
                cur.execute("""
                    SELECT v.plate_number, t.type_name
                    FROM vehicles v
                    JOIN vehicle_type t ON v.type_id = t.type_id
                """)
                vehicles_data = cur.fetchall()

                # Bir pandas dataframe'e dönüştürelim
                vehicles_df = pd.DataFrame(vehicles_data, columns=["Plaka", "Tip"])

            except Exception as e:
                st.error(f"Araçlar listelenirken hata oluştu: {e}")
                
            
            plate_list = vehicles_df["Plaka"].tolist()
            selected_plate = st.selectbox("Silmek istediğiniz aracı seçin:", plate_list, None)

            if st.button("Aracı Sil"):
                if selected_plate:
                    delete_query = "DELETE FROM vehicles WHERE plate_number = %s"
                    cur.execute(delete_query, (selected_plate,))
                    conn.commit()
                    st.success(f"{selected_plate} plakalı araç başarıyla silindi!")
                    st.rerun()
        except Exception as e:
            st.error(f"Araç silinirken bir hata oluştu: {e}")
    
    


    cur.close()
    
    st.divider()

    st.subheader("Araç ve Plaka Tespit Sistemi")
    st.write("Aşağıdaki butonlarla araç ve plaka tespit pipeline'ını kontrol edebilirsiniz.")

    col3, col4 = st.columns(2)
    
    # PROCESS PID'yi kaydetmek için dosya adı
    PID_FILE = "process.pid"
    

    with col3:
        if st.button("Pipeline'ı Çalıştır"):
            try:
                # Script'i çalıştır ve PID'yi kaydet
                process = subprocess.Popen(
                    ["python", "/Users/tunahanbg/Code/vscode_files/db_donem_sonu/final_sql_model_detect/pipeline_full_det.py"],  
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                # PID'yi bir dosyaya kaydet
                with open(PID_FILE, "w") as f:
                    f.write(str(process.pid))
                
                st.success("Pipeline başarıyla çalıştırıldı!")
            except Exception as e:
                st.error(f"Pipeline çalıştırılırken bir hata oluştu: {e}")
    
    with col4:
        
        if st.button("Pipeline'ı Durdur"):
            try:
                # PID'yi dosyadan oku
                if os.path.exists(PID_FILE):
                    with open(PID_FILE, "r") as f:
                        pid = int(f.read())
                    # İşlemi durdur
                    os.kill(pid, signal.SIGTERM)  # SIGTERM ile işlemi sonlandır
                    os.remove(PID_FILE)  # PID dosyasını sil
                    st.success("Pipeline başarıyla durduruldu!")
                else:
                    st.warning("Çalışan bir işlem bulunamadı!")
            except Exception as e:
                st.error(f"Pipeline durdurulurken bir hata oluştu: {e}")
                
    st.divider()
    
    
    # Çıkış Yap butonu
    if st.button("Çıkış Yap"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()
        
        

       