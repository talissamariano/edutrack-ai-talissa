"""Pagina inicial (Home) - dashboard exibido apos o login."""

import streamlit as st

st.title("🏠 Home")
st.write("Bem-vindo ao seu assistente academico!")

col1, col2 = st.columns(2)
col1.metric("Disciplinas Ativas", "0")
col2.metric("Tarefas Pendentes", "0")

st.info("Use o menu lateral para navegar entre as paginas. Futuros dashboards apareceram aqui.")
