"""Pagina de Gestao de Tarefas (academic_tasks) integrada ao Xano.

3 abas: Listar / Nova Tarefa / Historico.
A aba Listar tem dois modos de agrupamento (Disciplina ou Prazo).
No modo Prazo, as tarefas sao agrupadas por urgencia (Hoje, Esta semana, etc.).
Componentes Standard apenas (sem unsafe_allow_html).
"""

from __future__ import annotations

import datetime as _dt
from typing import Any

import streamlit as st

from lib import xano_client as xano

st.title("📝 Gestão de Tarefas")

# Flash de sucesso que sobrevive ao rerun
_flash = st.session_state.pop("task_flash_success", None)
if _flash:
    st.success(_flash)


STATUS_LABELS = {
    "pending": "Pendente",
    "in_progress": "Em andamento",
    "done": "Concluída",
}
STATUS_OPTIONS_CODE = ["pending", "in_progress", "done"]


def _handle_expiration() -> None:
    st.session_state["_session_expired_notice"] = True
    st.rerun()


def _parse_date(value: Any) -> _dt.date | None:
    """Aceita string ISO 'YYYY-MM-DD' ou ISO completa; devolve datetime.date."""
    if not value:
        return None
    if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
        return value
    text = str(value)
    try:
        return _dt.datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return _dt.date.fromisoformat(text[:10])
        except ValueError:
            return None


def _format_date_br(value: Any) -> str:
    d = _parse_date(value)
    return d.strftime("%d/%m/%Y") if d else "-"


def _is_overdue(task: dict) -> bool:
    if task.get("status") == "done":
        return False
    d = _parse_date(task.get("due_date"))
    return d is not None and d < _dt.date.today()


def _status_label(code: str | None) -> str:
    return STATUS_LABELS.get(code or "", code or "-")


# -----------------------------------------------------------------------------
# Carrega dados (uma vez por rerun)
# -----------------------------------------------------------------------------

def _load_subjects_map() -> dict[int, dict]:
    try:
        subjects = xano.subjects_search()
    except xano.SessionExpired:
        _handle_expiration()
        return {}
    except xano.XanoError as exc:
        st.error(str(exc))
        return {}
    return {s["id"]: s for s in subjects if "id" in s}


def _load_tasks(status: str | None, only_overdue: bool) -> list[dict]:
    try:
        return xano.tasks_list(
            status=status or None, only_overdue=only_overdue or None
        )
    except xano.SessionExpired:
        _handle_expiration()
        return []
    except xano.XanoError as exc:
        st.error(str(exc))
        return []


# -----------------------------------------------------------------------------
# Barra de filtros
# -----------------------------------------------------------------------------

with st.form("form_filtros_tarefas", clear_on_submit=False):
    col_titulo, col_status, col_overdue, col_btn = st.columns([3, 2, 2, 1])
    with col_titulo:
        termo_titulo = st.text_input(
            "Buscar por título",
            value=st.session_state.get("task_filtro_titulo", ""),
            placeholder="Ex.: Lista 1",
        )
    with col_status:
        status_label = st.selectbox(
            "Status",
            ["Todos", "Pendente", "Em andamento", "Concluída"],
            index=["Todos", "Pendente", "Em andamento", "Concluída"].index(
                st.session_state.get("task_filtro_status_label", "Todos")
            ),
        )
    with col_overdue:
        only_overdue = st.checkbox(
            "Apenas atrasadas",
            value=st.session_state.get("task_filtro_overdue", False),
        )
    with col_btn:
        st.write("")
        aplicar = st.form_submit_button("Filtrar", use_container_width=True)

if aplicar:
    st.session_state["task_filtro_titulo"] = termo_titulo
    st.session_state["task_filtro_status_label"] = status_label
    st.session_state["task_filtro_overdue"] = only_overdue

# Lê filtros persistidos
filtro_titulo = st.session_state.get("task_filtro_titulo", "")
filtro_status_label = st.session_state.get("task_filtro_status_label", "Todos")
filtro_overdue = st.session_state.get("task_filtro_overdue", False)
status_code = {
    "Pendente": "pending",
    "Em andamento": "in_progress",
    "Concluída": "done",
}.get(filtro_status_label)

subjects_map = _load_subjects_map()
todas_tasks = _load_tasks(status_code, filtro_overdue)

# Filtro client-side por título
if filtro_titulo:
    term = filtro_titulo.lower().strip()
    todas_tasks = [t for t in todas_tasks if term in (t.get("title") or "").lower()]

# Split ativas (subject não arquivado) vs históricas (subject arquivado)
def _subject_archived(task: dict) -> bool:
    subj = subjects_map.get(task.get("subject_id"))
    if not subj:
        return False
    return bool(subj.get("archived_at"))


tasks_ativas = [t for t in todas_tasks if not _subject_archived(t)]
tasks_historico = [t for t in todas_tasks if _subject_archived(t)]


# -----------------------------------------------------------------------------
# Dialogs
# -----------------------------------------------------------------------------

@st.dialog("Editar tarefa")
def _edit_dialog(task: dict, allow_subject_change: bool = True) -> None:
    active_subjects = [s for s in subjects_map.values() if not s.get("archived_at")]
    with st.form(f"form_edit_task_{task['id']}"):
        titulo = st.text_input("Título", value=task.get("title") or "")
        descricao = st.text_area("Descrição", value=task.get("description") or "")
        prazo_atual = _parse_date(task.get("due_date"))
        prazo = st.date_input(
            "Prazo", value=prazo_atual if prazo_atual else _dt.date.today()
        )
        status_atual = task.get("status") or "pending"
        novo_status_label = st.selectbox(
            "Status",
            ["Pendente", "Em andamento", "Concluída"],
            index=STATUS_OPTIONS_CODE.index(status_atual)
            if status_atual in STATUS_OPTIONS_CODE
            else 0,
        )
        novo_status = {
            "Pendente": "pending",
            "Em andamento": "in_progress",
            "Concluída": "done",
        }[novo_status_label]

        novo_subject_id: int | None = None
        if allow_subject_change and active_subjects:
            opcoes = active_subjects
            ids = [s["id"] for s in opcoes]
            try:
                idx = ids.index(task.get("subject_id"))
            except ValueError:
                idx = 0
            escolhido = st.selectbox(
                "Disciplina",
                options=range(len(opcoes)),
                index=idx,
                format_func=lambda i: opcoes[i].get("name", "-"),
            )
            novo_subject_id = opcoes[escolhido]["id"]

        salvar = st.form_submit_button("Salvar", type="primary")

    if salvar:
        try:
            xano.tasks_update(
                task["id"],
                title=titulo,
                description=descricao,
                due_date=prazo.isoformat() if prazo else None,
                status=novo_status,
                subject_id=novo_subject_id,
            )
            st.session_state["task_flash_success"] = (
                f"Tarefa '{titulo}' atualizada com sucesso."
            )
            st.rerun()
        except xano.SessionExpired:
            _handle_expiration()
        except xano.XanoError as exc:
            st.error(str(exc))


@st.dialog("Confirmar exclusão")
def _delete_dialog(task: dict) -> None:
    st.warning(
        f"Tem certeza que deseja excluir a tarefa '{task.get('title', '')}'? "
        "Esta ação não pode ser desfeita."
    )
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button(
            "Confirmar exclusão",
            key=f"confirm_del_task_{task['id']}",
            use_container_width=True,
            type="primary",
        ):
            try:
                xano.tasks_delete(task["id"])
                st.session_state["task_flash_success"] = (
                    f"Tarefa '{task.get('title', '')}' excluída."
                )
                st.rerun()
            except xano.SessionExpired:
                _handle_expiration()
            except xano.XanoError as exc:
                st.error(str(exc))
    with col_cancel:
        if st.button(
            "Cancelar",
            key=f"cancel_del_task_{task['id']}",
            use_container_width=True,
        ):
            st.rerun()


# -----------------------------------------------------------------------------
# Render helpers
# -----------------------------------------------------------------------------

def _render_task_row(
    task: dict,
    *,
    show_subject: bool = True,
    allow_complete: bool = True,
    key_prefix: str = "list",
) -> None:
    overdue = _is_overdue(task)
    with st.container(border=True):
        col_titulo, col_disc, col_prazo, col_status, col_done, col_ed, col_del = st.columns(
            [5, 3, 2, 2, 1, 1, 1]
        )

        titulo = task.get("title") or "(sem título)"
        prefix = "⚠️ " if overdue else ""
        col_titulo.markdown(f"**{prefix}{titulo}**")
        if task.get("description"):
            col_titulo.caption(task["description"])

        if show_subject:
            subj = subjects_map.get(task.get("subject_id")) or {}
            col_disc.write(subj.get("name") or "-")
        else:
            col_disc.write("")

        prazo_txt = _format_date_br(task.get("due_date"))
        if overdue:
            col_prazo.markdown(f":red[{prazo_txt}]")
        else:
            col_prazo.write(prazo_txt)

        col_status.write(_status_label(task.get("status")))

        if allow_complete and task.get("status") != "done":
            if col_done.button(
                "✓",
                key=f"{key_prefix}_complete_{task['id']}",
                help="Marcar como concluída",
                use_container_width=True,
            ):
                try:
                    xano.tasks_complete(task["id"])
                    st.session_state["task_flash_success"] = (
                        f"Tarefa '{titulo}' marcada como concluída."
                    )
                    st.rerun()
                except xano.SessionExpired:
                    _handle_expiration()
                except xano.XanoError as exc:
                    st.error(str(exc))
        else:
            col_done.write("")

        if col_ed.button(
            "✏️",
            key=f"{key_prefix}_edit_task_{task['id']}",
            help="Editar",
            use_container_width=True,
        ):
            _edit_dialog(task)

        if col_del.button(
            "🗑️",
            key=f"{key_prefix}_del_task_{task['id']}",
            help="Excluir",
            use_container_width=True,
        ):
            _delete_dialog(task)


def _render_header_row(show_subject: bool = True) -> None:
    h1, h2, h3, h4, _, _, _ = st.columns([5, 3, 2, 2, 1, 1, 1])
    h1.caption("**Título**")
    h2.caption("**Disciplina**" if show_subject else "")
    h3.caption("**Prazo**")
    h4.caption("**Status**")


def _sort_by_due_date(tasks: list[dict]) -> list[dict]:
    far_future = _dt.date(9999, 12, 31)

    def _key(t: dict) -> _dt.date:
        d = _parse_date(t.get("due_date"))
        return d if d else far_future

    return sorted(tasks, key=_key)


# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------

tab_listar, tab_nova, tab_historico = st.tabs(
    ["📋 Listar", "➕ Nova Tarefa", "📦 Histórico"]
)

# --------- Aba Listar ---------
with tab_listar:
    if not tasks_ativas:
        st.info("Nenhuma tarefa ativa com os filtros atuais.")
    else:
        agrupamento = st.radio(
            "Agrupar por",
            ["Disciplina", "Prazo"],
            horizontal=True,
            key="task_agrupamento",
        )

        if agrupamento == "Disciplina":
            por_subject: dict[int, list[dict]] = {}
            for t in tasks_ativas:
                por_subject.setdefault(t.get("subject_id") or 0, []).append(t)
            for sid, ts in por_subject.items():
                subj_name = (subjects_map.get(sid) or {}).get("name") or "(sem disciplina)"
                st.subheader(subj_name)
                _render_header_row(show_subject=False)
                for t in _sort_by_due_date(ts):
                    _render_task_row(t, show_subject=False, key_prefix="list")
        else:  # Por Prazo: agrupamento por urgencia
            hoje = _dt.date.today()
            sete_dias = hoje + _dt.timedelta(days=7)
            quatorze_dias = hoje + _dt.timedelta(days=14)

            grupos: dict[str, list[dict]] = {
                "🔴 Atrasadas": [],
                "🟠 Hoje": [],
                "🟡 Esta semana (próximos 7 dias)": [],
                "🟢 Próximas 2 semanas": [],
                "🔵 Mais tarde": [],
                "⚪ Sem prazo definido": [],
                "✅ Concluídas": [],
            }

            for t in tasks_ativas:
                if t.get("status") == "done":
                    grupos["✅ Concluídas"].append(t)
                    continue
                d = _parse_date(t.get("due_date"))
                if d is None:
                    grupos["⚪ Sem prazo definido"].append(t)
                elif d < hoje:
                    grupos["🔴 Atrasadas"].append(t)
                elif d == hoje:
                    grupos["🟠 Hoje"].append(t)
                elif d <= sete_dias:
                    grupos["🟡 Esta semana (próximos 7 dias)"].append(t)
                elif d <= quatorze_dias:
                    grupos["🟢 Próximas 2 semanas"].append(t)
                else:
                    grupos["🔵 Mais tarde"].append(t)

            for titulo, lista in grupos.items():
                if not lista:
                    continue
                st.subheader(f"{titulo} — {len(lista)}")
                _render_header_row(show_subject=True)
                for t in _sort_by_due_date(lista):
                    _render_task_row(t, show_subject=True, key_prefix="list")


# --------- Aba Nova Tarefa ---------
with tab_nova:
    st.subheader("Cadastrar Nova Tarefa")
    active_subjects = [s for s in subjects_map.values() if not s.get("archived_at")]
    if not active_subjects:
        st.warning("Você precisa ter ao menos uma disciplina ativa para criar tarefas.")
    else:
        st.caption("Após salvar, abra a aba '📋 Listar' para ver a tarefa.")
        with st.form("form_nova_tarefa", clear_on_submit=True):
            titulo = st.text_input("Título *", placeholder="Ex.: Lista 1")
            descricao = st.text_area("Descrição", placeholder="Opcional")
            prazo = st.date_input("Prazo", value=_dt.date.today())
            ids = [s["id"] for s in active_subjects]
            subject_idx = st.selectbox(
                "Disciplina *",
                options=range(len(active_subjects)),
                format_func=lambda i: active_subjects[i].get("name", "-"),
            )
            status_label_novo = st.selectbox(
                "Status", ["Pendente", "Em andamento", "Concluída"], index=0
            )
            criar = st.form_submit_button("Salvar", type="primary")

        if criar:
            if not titulo.strip():
                st.error("Título é obrigatório.")
            else:
                try:
                    xano.tasks_create(
                        titulo.strip(),
                        subject_id=ids[subject_idx],
                        description=descricao or None,
                        due_date=prazo.isoformat() if prazo else None,
                        status={
                            "Pendente": "pending",
                            "Em andamento": "in_progress",
                            "Concluída": "done",
                        }[status_label_novo],
                    )
                    st.session_state["task_flash_success"] = (
                        f"Tarefa '{titulo}' cadastrada com sucesso."
                    )
                    st.rerun()
                except xano.SessionExpired:
                    _handle_expiration()
                except xano.XanoError as exc:
                    st.error(str(exc))


# --------- Aba Histórico ---------
with tab_historico:
    if not tasks_historico:
        st.info("Nenhuma tarefa de disciplinas arquivadas.")
    else:
        por_subject_hist: dict[int, list[dict]] = {}
        for t in tasks_historico:
            por_subject_hist.setdefault(t.get("subject_id") or 0, []).append(t)
        for sid, ts in por_subject_hist.items():
            subj_name = (subjects_map.get(sid) or {}).get("name") or "(sem disciplina)"
            with st.expander(f"📦 {subj_name} (arquivada) — {len(ts)} tarefa(s)"):
                _render_header_row(show_subject=False)
                for t in _sort_by_due_date(ts):
                    _render_task_row(
                        t, show_subject=False, allow_complete=False, key_prefix="hist"
                    )
