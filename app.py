"""Roteador principal do EduTrack AI.

Usa st.navigation (Streamlit 1.36+) para alternar entre dois conjuntos de
paginas com base no estado de autenticacao:

- Nao autenticado: apenas a pagina de login (`login.py`).
- Autenticado: home + paginas existentes (Disciplinas, Tarefas, Perfil).

Quando st.navigation eh usado, a auto-descoberta da pasta `pages/` eh
desativada, entao paginas internas so ficam acessiveis se registradas aqui.
"""

import streamlit as st

from lib import xano_client as xano

st.set_page_config(page_title="EduTrack AI", page_icon="🎓")

# Restaura a sessao a partir do cookie (persistencia entre reloads).
xano.restore_session()

# Aviso de expiracao vindo de outras paginas.
if st.session_state.pop("_session_expired_notice", False):
    st.warning("Sua sessao expirou. Faca login novamente.")

if xano.is_authenticated():
    user = st.session_state.get("user") or {}
    with st.sidebar:
        st.write(f"Usuario: {user.get('id', '?')}")
        if st.button("Sair", use_container_width=True):
            xano.clear_session()
            st.rerun()

    pages = [
        st.Page("home.py", title="Home", icon="🏠", default=True),
        st.Page("pages/1_📚_Disciplinas.py", title="Disciplinas", icon="📚"),
        st.Page("pages/2_📝_Tarefas.py", title="Tarefas", icon="📝"),
        st.Page("pages/3_👤_Perfil.py", title="Perfil", icon="👤"),
    ]
else:
    pages = [st.Page("login.py", title="Entrar", icon="🔐", default=True)]

pg = st.navigation(pages)
pg.run()
