"""Pagina de Gestao de Disciplinas (v2).

3 abas: Listar ativas / Nova Disciplina / Arquivadas.
Layout em linhas com st.container + st.columns; sem unsafe_allow_html.
Componentes nativos: st.tabs, st.columns, st.form, st.text_input,
st.number_input, st.text_area, st.checkbox, st.button, st.container,
st.dialog, st.error, st.success.
"""

import datetime as _dt

import streamlit as st

from lib import xano_client as xano
from lib.dashboard_utils import (
    index_tasks_by_subject,
    is_overdue,
    is_upcoming,
    subject_progress,
)

st.title("📚 Gestão de Disciplinas")

# Flash de sucesso (sobrevive ao rerun)
_flash = st.session_state.pop("disc_flash_success", None)
if _flash:
    st.success(_flash)


def _handle_expiration() -> None:
    st.session_state["_session_expired_notice"] = True
    st.rerun()


def _load_subjects(name: str | None, only_overdue: bool) -> list[dict]:
    try:
        return xano.subjects_search(
            name=name or None, only_overdue=only_overdue or None
        )
    except xano.SessionExpired:
        _handle_expiration()
        return []
    except xano.XanoError as exc:
        st.error(str(exc))
        return []


# -----------------------------------------------------------------------------
# Barra de busca / filtros (aplica em ambas as abas)
# -----------------------------------------------------------------------------

with st.form("form_busca", clear_on_submit=False):
    col_nome, col_filtro, col_btn = st.columns([3, 2, 1])
    with col_nome:
        termo = st.text_input(
            "Buscar por nome",
            value=st.session_state.get("disc_busca_nome", ""),
            placeholder="Ex.: Cálculo",
        )
    with col_filtro:
        atrasadas = st.checkbox(
            "Apenas com tarefas atrasadas",
            value=st.session_state.get("disc_busca_atrasadas", False),
        )
    with col_btn:
        st.write("")
        buscar = st.form_submit_button("Buscar", use_container_width=True)

if buscar:
    st.session_state["disc_busca_nome"] = termo
    st.session_state["disc_busca_atrasadas"] = atrasadas

filtro_nome = st.session_state.get("disc_busca_nome", "")
filtro_atrasadas = st.session_state.get("disc_busca_atrasadas", False)
todas_disciplinas = _load_subjects(filtro_nome, filtro_atrasadas)

# Carrega tarefas do usuario para calcular progresso e sinais por disciplina.
def _load_all_tasks() -> list[dict]:
    try:
        return xano.tasks_list() or []
    except xano.SessionExpired:
        _handle_expiration()
        return []
    except xano.XanoError:
        return []


_all_tasks = _load_all_tasks()
_tasks_by_subject = index_tasks_by_subject(_all_tasks)
_today = _dt.date.today()

# Split client-side ativas vs arquivadas pelo campo archived_at
ativas = [s for s in todas_disciplinas if not s.get("archived_at")]
arquivadas = [s for s in todas_disciplinas if s.get("archived_at")]


# -----------------------------------------------------------------------------
# Dialogs
# -----------------------------------------------------------------------------

@st.dialog("Editar disciplina")
def _edit_dialog(subject: dict) -> None:
    with st.form(f"form_edit_{subject['id']}"):
        nome = st.text_input("Nome", value=subject.get("name", ""))
        professor = st.text_input("Professor", value=subject.get("professor") or "")
        carga = st.number_input(
            "Carga horária (h)",
            min_value=0,
            step=1,
            value=int(subject.get("workload_hours") or 0),
        )
        semestre = st.number_input(
            "Semestre do curso",
            min_value=0,
            step=1,
            value=int(subject.get("semester") or 0),
        )
        descricao = st.text_area(
            "Descrição", value=subject.get("description") or ""
        )
        salvar = st.form_submit_button("Salvar", type="primary")

    if salvar:
        try:
            xano.subjects_update(
                subject["id"],
                name=nome,
                professor=professor,
                description=descricao,
                workload_hours=int(carga) if carga else None,
                semester=int(semestre) if semestre else None,
            )
            st.session_state["disc_flash_success"] = (
                f"Disciplina '{nome}' atualizada com sucesso."
            )
            st.rerun()
        except xano.SessionExpired:
            _handle_expiration()
        except xano.XanoError as exc:
            st.error(str(exc))


@st.dialog("Confirmar exclusão")
def _delete_dialog(subject: dict) -> None:
    st.warning(
        f"Tem certeza que deseja excluir a disciplina '{subject.get('name', '')}'? "
        "Esta ação não pode ser desfeita."
    )
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button(
            "Confirmar exclusão",
            key=f"confirm_del_{subject['id']}",
            use_container_width=True,
            type="primary",
        ):
            try:
                xano.subjects_delete(subject["id"])
                st.session_state["disc_flash_success"] = (
                    f"Disciplina '{subject.get('name', '')}' excluída."
                )
                st.rerun()
            except xano.SessionExpired:
                _handle_expiration()
            except xano.XanoError as exc:
                st.error(str(exc))
    with col_cancel:
        if st.button(
            "Cancelar", key=f"cancel_del_{subject['id']}", use_container_width=True
        ):
            st.rerun()


# -----------------------------------------------------------------------------
# Render helpers (linha por disciplina)
# -----------------------------------------------------------------------------

def _format_int(value) -> str:
    return str(value) if value not in (None, "") else "-"


def _render_active_row(subject: dict) -> None:
    tasks_da_disciplina = _tasks_by_subject.get(subject.get("id"), [])
    prog = subject_progress(tasks_da_disciplina)
    pct = float(prog.get("percentage") or 0.0)
    n_atrasadas = sum(1 for t in tasks_da_disciplina if is_overdue(t, _today))
    n_proximas = sum(
        1 for t in tasks_da_disciplina if is_upcoming(t, _today) and not is_overdue(t, _today)
    )

    with st.container(border=True):
        (
            col_nome,
            col_prof,
            col_carga,
            col_sem,
            col_prog,
            col_sinais,
            col_ed,
            col_arq,
            col_del,
        ) = st.columns([3, 2, 1, 1, 2, 2, 1, 1, 1])
        col_nome.markdown(f"**{subject.get('name', '-')}**")
        col_nome.caption(subject.get("description") or "")
        col_prof.write(subject.get("professor") or "-")
        col_carga.write(_format_int(subject.get("workload_hours")) + "h")
        col_sem.write(_format_int(subject.get("semester")))

        col_prog.write(f"{pct:.0f}%")
        col_prog.progress(min(max(pct / 100.0, 0.0), 1.0))

        sinais = []
        if n_atrasadas > 0:
            sinais.append(f"⚠️ {n_atrasadas} atrasada(s)")
        if n_proximas > 0:
            sinais.append(f"📅 {n_proximas} próxima(s)")
        col_sinais.write("\n\n".join(sinais) if sinais else "")

        if col_ed.button(
            "✏️", key=f"edit_{subject['id']}", help="Editar", use_container_width=True
        ):
            _edit_dialog(subject)
        if col_arq.button(
            "📦", key=f"arq_{subject['id']}", help="Arquivar", use_container_width=True
        ):
            try:
                xano.subjects_archive(subject["id"])
                st.session_state["disc_flash_success"] = (
                    f"Disciplina '{subject.get('name', '')}' arquivada."
                )
                st.rerun()
            except xano.SessionExpired:
                _handle_expiration()
            except xano.XanoError as exc:
                st.error(str(exc))
        if col_del.button(
            "🗑️", key=f"del_{subject['id']}", help="Excluir", use_container_width=True
        ):
            _delete_dialog(subject)


def _render_archived_row(subject: dict) -> None:
    with st.container(border=True):
        col_nome, col_prof, col_carga, col_sem, col_un, col_del = st.columns(
            [3, 3, 1, 1, 1, 1]
        )
        col_nome.markdown(f"**{subject.get('name', '-')}**")
        col_nome.caption(subject.get("description") or "")
        col_prof.write(subject.get("professor") or "-")
        col_carga.write(_format_int(subject.get("workload_hours")) + "h")
        col_sem.write(_format_int(subject.get("semester")))

        if col_un.button(
            "📤",
            key=f"un_{subject['id']}",
            help="Desarquivar",
            use_container_width=True,
        ):
            try:
                xano.subjects_unarchive(subject["id"])
                st.session_state["disc_flash_success"] = (
                    f"Disciplina '{subject.get('name', '')}' desarquivada."
                )
                st.rerun()
            except xano.SessionExpired:
                _handle_expiration()
            except xano.XanoError as exc:
                st.error(str(exc))
        if col_del.button(
            "🗑️",
            key=f"del_arq_{subject['id']}",
            help="Excluir",
            use_container_width=True,
        ):
            _delete_dialog(subject)


# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------

tab_ativas, tab_nova, tab_arquivadas = st.tabs(
    ["📋 Listar ativas", "➕ Nova Disciplina", "📦 Arquivadas"]
)

with tab_ativas:
    if not ativas:
        st.info("Nenhuma disciplina ativa com os filtros atuais.")
    else:
        # Cabecalho de colunas (alinhado a _render_active_row)
        h1, h2, h3, h4, h5, h6, _, _, _ = st.columns([3, 2, 1, 1, 2, 2, 1, 1, 1])
        h1.caption("**Nome**")
        h2.caption("**Professor**")
        h3.caption("**Carga**")
        h4.caption("**Sem.**")
        h5.caption("**Progresso**")
        h6.caption("**Sinais**")
        for s in ativas:
            _render_active_row(s)

with tab_nova:
    st.subheader("Cadastrar Nova Disciplina")
    st.caption("Após salvar, abra a aba '📋 Listar ativas' para ver o novo registro.")
    with st.form("form_nova_disciplina", clear_on_submit=True):
        nome = st.text_input("Nome da Disciplina *", placeholder="Ex.: Cálculo I")
        professor = st.text_input("Professor *", placeholder="Ex.: Oriel Marques")
        col_a, col_b = st.columns(2)
        with col_a:
            carga = st.number_input(
                "Carga horária (h)", min_value=0, step=1, value=0
            )
        with col_b:
            semestre = st.number_input(
                "Semestre do curso", min_value=0, step=1, value=0
            )
        descricao = st.text_area("Descrição", placeholder="Opcional")
        criar = st.form_submit_button("Salvar", type="primary")

    if criar:
        if not nome.strip() or not professor.strip():
            st.error("Nome e Professor são obrigatórios.")
        else:
            try:
                xano.subjects_create(
                    nome.strip(),
                    professor.strip(),
                    descricao or "",
                    workload_hours=int(carga) if carga else None,
                    semester=int(semestre) if semestre else None,
                )
                st.session_state["disc_flash_success"] = (
                    f"Disciplina '{nome}' cadastrada com sucesso."
                )
                st.rerun()
            except xano.SessionExpired:
                _handle_expiration()
            except xano.XanoError as exc:
                st.error(str(exc))

with tab_arquivadas:
    if not arquivadas:
        st.info("Nenhuma disciplina arquivada.")
    else:
        h1, h2, h3, h4, _, _ = st.columns([3, 3, 1, 1, 1, 1])
        h1.caption("**Nome**")
        h2.caption("**Professor**")
        h3.caption("**Carga**")
        h4.caption("**Sem.**")
        for s in arquivadas:
            _render_archived_row(s)
