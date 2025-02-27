import streamlit as st
import main_page 

def show_login_page():

    st.set_page_config(
        page_title="Kullanıcı Giriş",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    st.header("Otopark Yönetim Sistemine Hoş Geldiniz!")

    with st.form("login_form"):
        username = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adınızı giriniz")
        password = st.text_input("🔒 Şifre", placeholder="Şifrenizi giriniz", type="password")
        login_button = st.form_submit_button("Giriş Yap")

    if login_button:
        user_info = main_page.get_user_info(username.strip(), password.strip())
        user_id = main_page.get_user_id(username.strip(), password.strip())
        
        if user_info and user_id is not None:
            st.session_state.username = user_info[0]  
            st.session_state.role = user_info[1]      
            st.session_state.user_id = user_id        
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")
