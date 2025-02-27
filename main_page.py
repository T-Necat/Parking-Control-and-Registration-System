import streamlit as st
import psycopg2
from psycopg2 import sql
from apps import admin, manager, user, login
from config import DB_CONFIG

def get_db_connection():
    if "db_connection" not in st.session_state:
        st.session_state.db_connection = psycopg2.connect(**DB_CONFIG)
    return st.session_state.db_connection

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
        
        user_info = cur.fetchone()
        return user_info if user_info else None
    except Exception as e:
        st.error(f"Veritabanı hatası: {e}")
        return None
    finally:
        cur.close()

def get_user_id(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT u.user_id
            FROM users u
            WHERE u.user_name = %s AND u.password = %s;
        """, (username, password))
        
        user_id = cur.fetchone()
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

if not st.session_state.logged_in:
    login.show_login_page()
else:
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
