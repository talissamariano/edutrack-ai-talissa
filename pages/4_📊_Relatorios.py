"""Página Relatórios: exporta Tarefas, Disciplinas e Snapshot em CSV e PDF.

Componentes Standard apenas (sem unsafe_allow_html). Toda geração in-memory
via helpers puros em `lib/exporters.py` — sem novos endpoints Xano.
"""

from __future__ import annotations

import datetime as _dt

import streamlit as st

from lib import xano_client as xano
from lib.exporters import (
    dashboard_snapshot_to_csv,
    dashboard_snapshot_to_pdf,
    subjects_to_csv,
    subjects_to_pdf,
    tasks_to_csv,
    tasks_to_pdf,
)

st.title("📊 Relatórios")
st.caption("Exporte seus dados acadêmicos em CSV ou PDF.")


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


subjects = _load_subjects()
tasks = _load_tasks()
hoje = _dt.date.today()
hoje_iso = hoje.isoformat()

subjects_by_id = {s["id"]: s for s in subjects if "id" in s}

STATUS_LABELS = {"pending": "Pendente", "in_progress": "Em andamento", "done": "Concluída"}
PRIORITY_LABELS = {"low": "Baixa", "medium": "Média", "high": "Alta"}

# -----------------------------------------------------------------------------
# Tarefas
# -----------------------------------------------------------------------------

st.subheader("📝 Tarefas")

if not tasks:
    st.info("Você ainda não tem tarefas cadastradas.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        disc_opts = ["Todas"] + [s.get("name") or "(sem nome)" for s in subjects]
        disc_sel = st.selectbox("Disciplina", disc_opts, key="rel_disc")
    with col2:
        status_sel = st.multiselect(
            "Status",
            options=list(STATUS_LABELS.values()),
            default=[],
            key="rel_status",
        )
    with col3:
        prio_sel = st.multiselect(
            "Prioridade",
            options=list(PRIORITY_LABELS.values()),
            default=[],
            key="rel_prio",
        )

    status_codes = {k for k, v in STATUS_LABELS.items() if v in status_sel}
    prio_codes = {k for k, v in PRIORITY_LABELS.items() if v in prio_sel}

    filtrar_periodo = st.toggle("Filtrar por período", key="rel_periodo_toggle")
    date_from: _dt.date | None = None
    date_to: _dt.date | None = None
    if filtrar_periodo:
        cp1, cp2 = st.columns(2)
        date_from = cp1.date_input("De", value=None, key="rel_date_from", format="DD/MM/YYYY")
        date_to = cp2.date_input("Até", value=None, key="rel_date_to", format="DD/MM/YYYY")
        st.caption("Tarefas sem prazo definido são excluídas quando o filtro está ativo.")

    def _parse_date_rel(v) -> _dt.date | None:
        if not v:
            return None
        try:
            return _dt.date.fromisoformat(str(v)[:10])
        except ValueError:
            return None

    tasks_filt = tasks
    if disc_sel != "Todas":
        subj_id = next(
            (s["id"] for s in subjects if (s.get("name") or "(sem nome)") == disc_sel),
            None,
        )
        tasks_filt = [t for t in tasks_filt if t.get("subject_id") == subj_id]
    if status_codes:
        tasks_filt = [t for t in tasks_filt if t.get("status") in status_codes]
    if prio_codes:
        tasks_filt = [t for t in tasks_filt if t.get("priority") in prio_codes]
    if filtrar_periodo:
        def _in_range(t: dict) -> bool:
            d = _parse_date_rel(t.get("due_date"))
            if d is None:
                return False
            if date_from and d < date_from:
                return False
            if date_to and d > date_to:
                return False
            return True
        tasks_filt = [t for t in tasks_filt if _in_range(t)]

    st.caption(f"{len(tasks_filt)} tarefa(s) no escopo atual.")

    if not tasks_filt:
        st.info("Nenhuma tarefa para exportar com os filtros atuais.")
    else:
        c1, c2 = st.columns(2)
        c1.download_button(
            "📄 Baixar CSV",
            data=tasks_to_csv(tasks_filt, subjects_by_id),
            file_name=f"edutrack_tarefas_{hoje_iso}.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_tasks_csv",
        )
        c2.download_button(
            "📕 Baixar PDF",
            data=tasks_to_pdf(tasks_filt, subjects_by_id),
            file_name=f"edutrack_tarefas_{hoje_iso}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="dl_tasks_pdf",
        )

st.markdown("---")

# -----------------------------------------------------------------------------
# Disciplinas
# -----------------------------------------------------------------------------

st.subheader("📚 Disciplinas")

if not subjects:
    st.info("Você ainda não tem disciplinas cadastradas.")
else:
    st.caption(f"{len(subjects)} disciplina(s) no total.")
    c1, c2 = st.columns(2)
    c1.download_button(
        "📄 Baixar CSV",
        data=subjects_to_csv(subjects, tasks),
        file_name=f"edutrack_disciplinas_{hoje_iso}.csv",
        mime="text/csv",
        use_container_width=True,
        key="dl_subj_csv",
    )
    c2.download_button(
        "📕 Baixar PDF",
        data=subjects_to_pdf(subjects, tasks),
        file_name=f"edutrack_disciplinas_{hoje_iso}.pdf",
        mime="application/pdf",
        use_container_width=True,
        key="dl_subj_pdf",
    )

st.markdown("---")

# -----------------------------------------------------------------------------
# Snapshot do Dashboard
# -----------------------------------------------------------------------------

st.subheader("📈 Snapshot do Dashboard")
st.caption("Resumo consolidado: métricas + progresso por disciplina + próximas tarefas.")

if not subjects and not tasks:
    st.info("Sem dados para gerar o snapshot.")
else:
    c1, c2 = st.columns(2)
    c1.download_button(
        "📄 Baixar CSV",
        data=dashboard_snapshot_to_csv(subjects, tasks, hoje),
        file_name=f"edutrack_resumo_{hoje_iso}.csv",
        mime="text/csv",
        use_container_width=True,
        key="dl_dash_csv",
    )
    c2.download_button(
        "📕 Baixar PDF",
        data=dashboard_snapshot_to_pdf(subjects, tasks, hoje),
        file_name=f"edutrack_resumo_{hoje_iso}.pdf",
        mime="application/pdf",
        use_container_width=True,
        key="dl_dash_pdf",
    )
