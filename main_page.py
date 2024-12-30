import streamlit as st
import psycopg2
from psycopg2 import sql
from apps import admin, manager, user, login
from config import DB_CONFIG

# Veritabanı bağlantı fonksiyonu
def get_db_connection():
    if "db_connection" not in st.session_state:
        st.session_state.db_connection = psycopg2.connect(**DB_CONFIG)
    return st.session_state.db_connection

# 1) Kullanıcı adı ve şifreye göre sadece user_name ve role_name döndüren fonksiyon
def get_user_info(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT u.user_name, r.role_name
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
            WHERE u.user_name = %s AND u.password = %s;
        """, (username, password))
        
        user_info = cur.fetchone()  # (user_name, role_name) şeklinde bir tuple döner
        return user_info if user_info else None
    except Exception as e:
        st.error(f"Veritabanı hatası: {e}")
        return None
    finally:
        cur.close()

# 2) Kullanıcı adı ve şifreye göre sadece user_id döndüren fonksiyon
def get_user_id(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT u.user_id
            FROM users u
            WHERE u.user_name = %s AND u.password = %s;
        """, (username, password))
        
        user_id = cur.fetchone()  # (user_id,) şeklinde bir tuple döner
        return user_id[0] if user_id else None
    except Exception as e:
        st.error(f"Veritabanı hatası: {e}")
        return None
    finally:
        cur.close()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# Uygulama Akışı
if not st.session_state.logged_in:
    # Giriş yapılmadıysa login sayfasını göster
    login.show_login_page()
else:
    # Giriş yapıldıysa role göre sayfayı göster
    if st.session_state.role == "Admin":
        admin.show_admin_page()
    elif st.session_state.role == "Manager":
        manager.show_manager_page()
    elif st.session_state.role == "User":
        user.show_user_page()
    else:
        st.error("Bilinmeyen bir role sahipsiniz!")
        if st.button("Çıkış Yap"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()
