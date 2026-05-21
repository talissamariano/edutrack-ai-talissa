"""Pagina de Perfil: exibe e permite editar nome e e-mail.

O gate de autenticacao eh feito pelo roteador (app.py): esta pagina so eh
acessivel apos login. Em caso de token expirar durante o uso, sinalizamos e
o roteador volta para a tela de login no proximo rerun.
"""

import streamlit as st

from lib import xano_client as xano

st.title("👤 Meu Perfil")


def _handle_expiration() -> None:
    st.session_state["_session_expired_notice"] = True
    st.rerun()


# Carrega o perfil atual via /auth/me
try:
    profile = xano.me()
except xano.SessionExpired:
    _handle_expiration()
    st.stop()
except xano.XanoError as exc:
    st.error(str(exc))
    st.stop()

st.subheader("Dados atuais")
st.write(f"**Nome:** {profile.get('name', '-')}")
st.write(f"**E-mail:** {profile.get('email', '-')}")

st.markdown("---")
st.subheader("Editar perfil")
with st.form("form_profile"):
    new_name = st.text_input("Nome", value=profile.get("name", ""))
    new_email = st.text_input("E-mail", value=profile.get("email", ""))
    submitted = st.form_submit_button("Salvar")

if submitted:
    try:
        updated = xano.update_profile(name=new_name, email=new_email)
        if isinstance(updated, dict) and "id" in updated:
            st.session_state["user"] = {"id": updated["id"]}
        st.success("Perfil atualizado.")
        st.rerun()
    except xano.SessionExpired:
        _handle_expiration()
    except xano.XanoError as exc:
        st.error(str(exc))
