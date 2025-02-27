import streamlit as st
import pandas as pd
import main_page
import re

def show_user_page():
    st.set_page_config(page_title="User Sayfası", layout="wide")

    st.title("User Sayfası")
    st.success(f"Hoş geldiniz!")
    
    conn = main_page.get_db_connection()
    cur = conn.cursor()

    user_id = st.session_state.user_id

    cur.execute("SELECT type_id, type_name FROM vehicle_type;")
    types = cur.fetchall() 

    type_names = [t[1] for t in types]

    st.write("*Araç Ekle*")
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
            selected_type_id = None
            for t_id, t_name in types:
                if t_name == selected_type_name:
                    selected_type_id = t_id
                    break
            
            try:
                check_query = "SELECT COUNT(*) FROM vehicles WHERE plate_number = %s;"
                cur.execute(check_query, (plate_input,))
                exists = cur.fetchone()[0]

                if exists > 0:
                    st.error(f"{plate_input} plakalı araç zaten sistemde mevcut!")
                else:
                    price_query = "SELECT price FROM vehicle_type WHERE type_id = %s;"
                    cur.execute(price_query, (selected_type_id,))
                    result = cur.fetchone()

                    if not result:
                        st.error("Seçilen araç tipine ait fiyat bilgisi bulunamadı!")
                    else:
                        vehicle_price = result[0]

                        insert_vehicle_query = """
                            INSERT INTO vehicles (plate_number, type_id, is_detected)
                            VALUES (%s, %s, %s);
                        """
                        cur.execute(insert_vehicle_query, (plate_input, selected_type_id, False))

                        insert_record_query = """
                            INSERT INTO parking_records (plate_number, entry_time, cost, user_id)
                            VALUES (%s, NOW(), %s, %s);
                        """
                        cur.execute(insert_record_query, (plate_input, vehicle_price, user_id))

                        conn.commit()
                        st.success(f"{plate_input} plakalı araç başarıyla eklendi!")
            except Exception as e:
                conn.rollback()
                st.error(f"Araç eklenirken hata oluştu: {e}")

    
    st.divider()

    st.write("### Kayıtlarınız")
    try:
        query = """
            SELECT record_id, plate_number, entry_time, cost 
            FROM parking_records 
            WHERE user_id = %s
        """
        cur.execute(query, (user_id,))
        records = cur.fetchall()

        if records:
            records_df = pd.DataFrame(records, columns=["Record ID", "Plate Number", "Entry Time", "Cost"])
            st.dataframe(records_df, use_container_width=True)
        else:
            st.info("Henüz size ait herhangi bir kayıt bulunamadı.")
    except Exception as e:
        st.error(f"Kayıtlar alınırken hata oluştu: {e}")

    st.divider()
    
    cur.close()
    if st.button("Çıkış Yap"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()
