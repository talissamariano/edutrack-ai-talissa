"""Pagina inicial (Home) com dashboard e tela de boas-vindas.

- Sem disciplinas: tela de boas-vindas com CTA.
- Com disciplinas: 4 metricas + barra de progresso + lista das proximas tarefas.
"""

from __future__ import annotations

import datetime as _dt

import streamlit as st

from lib import xano_client as xano
from lib.dashboard_utils import (
    is_overdue,
    subject_progress,
    upcoming_tasks,
)

st.title("🏠 Home")


def _handle_expiration() -> None:
    st.session_state["_session_expired_notice"] = True
    st.rerun()


def _load_subjects() -> list[dict]:
    try:
        return xano.subjects_search() or []
    except xano.SessionExpired:
        _handle_expiration()
        return []
    except xano.XanoError as exc:
        st.error(f"Erro ao carregar disciplinas: {exc}")
        return []


def _load_tasks() -> list[dict]:
    try:
        return xano.tasks_list() or []
    except xano.SessionExpired:
        _handle_expiration()
        return []
    except xano.XanoError as exc:
        st.error(f"Erro ao carregar tarefas: {exc}")
        return []


def _format_date_br(value) -> str:
    if not value:
        return "-"
    text = str(value)[:10]
    try:
        return _dt.date.fromisoformat(text).strftime("%d/%m/%Y")
    except ValueError:
        return text


subjects = _load_subjects()
tasks = _load_tasks()

# -----------------------------------------------------------------------------
# Tela de boas-vindas (usuario novo, sem nenhuma disciplina)
# -----------------------------------------------------------------------------

if not subjects:
    st.subheader("👋 Bem-vindo ao EduTrack AI!")
    st.write(
        "Voce ainda nao tem disciplinas cadastradas. Comece adicionando suas "
        "materias do semestre — depois, voce podera registrar tarefas vinculadas "
        "a cada uma delas."
    )
    st.info(
        "💡 **Como funciona:**\n"
        "1. Cadastre suas disciplinas (nome, professor, carga horaria, semestre)\n"
        "2. Adicione tarefas com prazo vinculadas a cada disciplina\n"
        "3. Acompanhe seu progresso aqui na Home"
    )
    # st.page_link aponta para o arquivo registrado em app.py via st.navigation
    st.page_link(
        "pages/1_📚_Disciplinas.py",
        label="📚 Cadastrar minha primeira disciplina",
        icon="➡️",
    )
    st.stop()


# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------

hoje = _dt.date.today()
ativas = [s for s in subjects if not s.get("archived_at")]
pendentes = [t for t in tasks if t.get("status") != "done"]
atrasadas = [t for t in pendentes if is_overdue(t, hoje)]
progresso_geral = subject_progress(tasks)
percentage = float(progresso_geral.get("percentage") or 0.0)

st.subheader("Visão geral")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📚 Disciplinas ativas", len(ativas))
col2.metric("📝 Tarefas pendentes", len(pendentes))
col3.metric("⚠️ Tarefas atrasadas", len(atrasadas))
col4.metric("✅ Progresso geral", f"{percentage:.0f}%")

st.progress(min(max(percentage / 100.0, 0.0), 1.0))
st.caption(
    f"{progresso_geral.get('completed', 0)} concluída(s) de "
    f"{progresso_geral.get('total', 0)} tarefa(s)."
)

st.markdown("---")

# -----------------------------------------------------------------------------
# Proximas tarefas
# -----------------------------------------------------------------------------

st.subheader("📅 Próximas tarefas")
proximas = upcoming_tasks(tasks, today=hoje, limit=5)

if not proximas:
    st.success("🎉 Nenhuma tarefa pendente. Aproveite!")
else:
    subjects_by_id = {s["id"]: s for s in subjects if "id" in s}
    rows = []
    for t in proximas:
        subj = subjects_by_id.get(t.get("subject_id")) or {}
        prazo_txt = _format_date_br(t.get("due_date"))
        if is_overdue(t, hoje):
            prazo_txt = f"⚠️ {prazo_txt}"
        rows.append(
            {
                "Título": t.get("title") or "(sem título)",
                "Disciplina": subj.get("name") or "-",
                "Prazo": prazo_txt,
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.caption("Mostrando até 5 tarefas pendentes mais próximas. Veja todas em 📝 Tarefas.")
