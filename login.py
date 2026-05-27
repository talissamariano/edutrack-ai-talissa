"""Tela dedicada de Login / Cadastro / Esqueci a senha.

Eh exibida pelo roteador (app.py) quando o usuario nao esta autenticado.
Layout em colunas: esquerda = identidade visual, direita = formularios.
"""

import streamlit as st

from lib import xano_client as xano

col_marca, col_forms = st.columns([1.1, 1])

with col_marca:
    st.title("🎓 EduTrack AI")
    st.markdown("**Organize sua vida acadêmica de forma simples e inteligente.**")
    st.caption("EduTrack AI · 2026")

with col_forms:
    tab_login, tab_signup, tab_reset = st.tabs(["Entrar", "Cadastrar", "Esqueci a senha"])

    with tab_login:
        with st.form("form_login"):
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        if submitted:
            try:
                payload = xano.login(email, password)
                xano.store_session(payload)
                st.success("Login realizado.")
                st.rerun()
            except xano.XanoError as exc:
                st.error(str(exc))

    with tab_signup:
        with st.form("form_signup"):
            name = st.text_input("Nome")
            email = st.text_input("E-mail", key="signup_email")
            password = st.text_input("Senha", type="password", key="signup_password")
            submitted = st.form_submit_button("Criar conta", use_container_width=True)
        if submitted:
            try:
                payload = xano.signup(name, email, password)
                xano.store_session(payload)
                st.success("Conta criada e sessao iniciada.")
                st.rerun()
            except xano.XanoError as exc:
                st.error(str(exc))

    with tab_reset:
        st.caption(
            "Voce recebera um magic link por e-mail. Apos clicar no link, retorne "
            "ao app para definir a nova senha."
        )
        with st.form("form_reset"):
            email = st.text_input("E-mail da conta", key="reset_email")
            submitted = st.form_submit_button("Enviar link", use_container_width=True)
        if submitted:
            try:
                xano.request_reset(email)
                st.success("Se o e-mail existir, um link foi enviado.")
            except xano.XanoError as exc:
                st.error(str(exc))
