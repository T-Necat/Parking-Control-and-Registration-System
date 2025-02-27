import streamlit as st
import pandas as pd
import main_page
import re

def show_admin_page():
    st.set_page_config(page_title="Admin Sayfası", layout="wide")
    st.title("Admin Sayfası")
    st.success(f"Hoş geldiniz!")

    conn = main_page.get_db_connection()
    cur = conn.cursor()
    
    user_id = st.session_state.user_id

    st.divider()
    
    col1, col2 = st.columns(2)

    
    with col1:
        st.write("### Yeni Kullanıcı Ekle")
        new_username = st.text_input("Kullanıcı Adı:", key="new_username")
        new_password = st.text_input("Şifre:", type="password", key="new_password")

        role_options = {"Manager": 2, "User": 3}
        selected_role_name = st.selectbox("Rol Seçiniz:", list(role_options.keys()), key="role_select", index= None)

        if st.button("Kullanıcı Ekle", key="add_user"):
            if new_username.strip() == "" or new_password.strip() == "":
                st.error("Kullanıcı adı ve şifre boş olamaz!")
            elif selected_role_name is None:
                st.error("Lütfen bir rol seçiniz!")
            else:
                selected_role_id = role_options[selected_role_name]

                try:
                    insert_query = """
                        INSERT INTO users (user_name, password, role_id)
                        VALUES (%s, %s, %s);
                    """
                    cur.execute(insert_query, (new_username, new_password, selected_role_id))
                    conn.commit()
                    st.success("Kullanıcı başarıyla eklendi!")

                except Exception as e:
                    conn.rollback()
                    if "duplicate key value violates unique constraint" in str(e):
                        st.error("Bu kullanıcı adı alınmış!")
                    else:
                        st.error(f"Kullanıcı eklenirken hata oluştu: {e}")

    with col2:
        st.write("### Kullanıcı Sil")
        cur.execute("SELECT user_id, user_name FROM Users WHERE user_name NOT IN ('admin', 'model');")
        users_data = cur.fetchall()

        if users_data:
            user_options = {f"{user[1]} (ID: {user[0]})": user[0] for user in users_data}
            selected_user = st.selectbox("Silinecek Kullanıcıyı Seçin:", list(user_options.keys()), key="delete_user_select", index= None)

            if st.button("Kullanıcıyı Sil", key="delete_user"):
                if selected_user is None:
                    st.error("Lütfen bir kullanıcı seçiniz!")
                else:
                    try:
                        delete_query = "DELETE FROM users WHERE user_id = %s;"
                        cur.execute(delete_query, (user_options[selected_user],))
                        conn.commit()
                        st.success(f"Kullanıcı başarıyla silindi: {selected_user}")

                    except Exception as e:
                        conn.rollback()
                        st.error(f"Kullanıcı silinirken hata oluştu: {e}")
        else:
            st.info("Silinecek kullanıcı bulunamadı.")
                
                
    st.divider()
    
    
    col5, col6 = st.columns(2)
    
    
    cur.execute("SELECT type_id, type_name FROM vehicle_type;")
    types = cur.fetchall()  
    
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
        
        
        try:
            cur.execute("""
                SELECT v.plate_number, t.type_name
                FROM vehicles v
                JOIN vehicle_type t ON v.type_id = t.type_id
            """)
            vehicles_data = cur.fetchall()

            vehicles_df = pd.DataFrame(vehicles_data, columns=["Plaka", "Tip"])

        except Exception as e:
            st.error(f"Araçlar listelenirken hata oluştu: {e}")
        
        st.write("#### Araç Silme İşlemi")
        try:
            plate_list = vehicles_df["Plaka"].tolist()
            selected_plate = st.selectbox("Silmek istediğiniz aracı seçin:", plate_list, None)
            
            sub_col1, sub_col2 = st.columns(2)
            
            with sub_col1:
                if st.button("Aracı Sil"):
                    if selected_plate is None:
                        st.error("Lütfen bir araç seçiniz!")
                    
                    try:
                        if selected_plate:
                            delete_query = "DELETE FROM vehicles WHERE plate_number = %s"
                            cur.execute(delete_query, (selected_plate,))
                            conn.commit()
                            st.success(f"{selected_plate} plakalı araç başarıyla silindi!")
                    except Exception as e:
                        st.error(f"Araçlar silinirken hata oluştu: {e}")
                    
            with sub_col2:
                if st.button("Tüm Araçları Sil"):
                    try:
                        cur.execute("DELETE FROM vehicles;")
                        conn.commit()
                        st.success("Tüm araçlar başarıyla silindi!")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Araçlar silinirken bir hata oluştu: {e}")
                    
                    
        except Exception as e:
            st.error(f"Araç silinirken bir hata oluştu: {e}")
            
            

    st.divider()
    
    
    
    
    cur.execute("SELECT user_id, user_name, password, role_id FROM Users WHERE user_name NOT IN ('admin', 'model');")
    users_data = cur.fetchall()
    df_users = pd.DataFrame(users_data, columns=["User ID", "User Name", "Password", "Role ID"])

    cur.execute("SELECT plate_number, type_id, is_detected FROM Vehicles;")
    vehicles_data = cur.fetchall()
    df_vehicles = pd.DataFrame(vehicles_data, columns=["Plate Number", "Type ID", "Is Detected?"])
    
    col3, col4 = st.columns(2)

    with col3:
        st.write("### Users Tablosu")
        st.dataframe(df_users, use_container_width=True, hide_index= True)

    with col4:
        st.write("### Vehicles Tablosu")
        st.dataframe(df_vehicles, use_container_width=True, hide_index= True)
        
    st.divider()
        
    cur.execute("SELECT record_id, plate_number, entry_time, cost, user_id FROM parking_records;")
    records_data = cur.fetchall()
    
    df_records = pd.DataFrame(records_data, columns=["Record ID", "Plate Number", "Entry Time", "Cost", "User ID"])

    st.write("### Parking Records")
    st.dataframe(df_records, use_container_width=True)
    
    if st.button("Tabloyu Sıfırla"):
        try:
            cur.execute("DELETE FROM parking_records;")
            conn.commit()
            st.success("Tablo başarıyla sıfırlandı!")
            st.rerun()  
        except Exception as e:
            conn.rollback()
            st.error(f"Tablo sıfırlanırken hata oluştu: {e}")

    cur.close()
    
    st.divider()
    
    # Çıkış butonu
    if st.button("Çıkış Yap"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

    