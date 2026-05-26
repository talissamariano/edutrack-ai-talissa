"""Pagina inicial (Home) com dashboard e tela de boas-vindas.

- Sem disciplinas: tela de boas-vindas com CTA.
- Com disciplinas: 4 metricas + barra de progresso + lista das proximas tarefas.
"""

from __future__ import annotations

import calendar as _calendar
import datetime as _dt

import altair as alt
import pandas as pd
import streamlit as st

from lib import xano_client as xano
from lib.dashboard_utils import (
    index_tasks_by_subject,
    is_overdue,
    subject_progress,
    upcoming_tasks,
)
from lib.quotes import quote_of_the_day

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


def _load_profile() -> dict:
    try:
        return xano.me() or {}
    except xano.SessionExpired:
        _handle_expiration()
        return {}
    except xano.XanoError:
        return {}


def _parse_birthday(value) -> _dt.date | None:
    if not value:
        return None
    text = str(value)[:10]
    try:
        return _dt.date.fromisoformat(text)
    except ValueError:
        return None


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
profile = _load_profile()

# -----------------------------------------------------------------------------
# Banner de aniversario (se hoje for o aniversario do usuario)
# -----------------------------------------------------------------------------

def _is_birthday_today(birthday: _dt.date, today: _dt.date) -> bool:
    """Aniversario hoje? Trata 29/fev em anos nao-bissextos celebrando 28/fev e 1/mar."""
    if (birthday.month, birthday.day) == (today.month, today.day):
        return True
    # 29/fev em ano nao-bissexto: celebra nos dois dias adjacentes.
    if (
        birthday.month == 2
        and birthday.day == 29
        and not _calendar.isleap(today.year)
    ):
        return (today.month, today.day) in ((2, 28), (3, 1))
    return False


birthday = _parse_birthday(profile.get("birthday"))
hoje_now = _dt.date.today()
if birthday and _is_birthday_today(birthday, hoje_now):
    nome = profile.get("name") or "estudante"
    st.success(f"🎉 Feliz aniversário, {nome}! Que seu dia seja incrível. 🎂")

# -----------------------------------------------------------------------------
# Post-it com a frase do dia
# -----------------------------------------------------------------------------

_quote = quote_of_the_day(hoje_now)
_quote_text = _quote.get("text", "")
_quote_author = _quote.get("author", "")
if _quote_author:
    st.info(f"💭 *{_quote_text}*  \n— **{_quote_author}**")
else:
    st.info(f"💭 *{_quote_text}*")

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
# Progresso por disciplina (barras verticais)
# -----------------------------------------------------------------------------

st.subheader("📊 Progresso por disciplina")
tasks_por_subject = index_tasks_by_subject(tasks)
linhas_chart: list[dict] = []
for s in ativas:
    nome = s.get("name") or "(sem nome)"
    tarefas_da_disc = tasks_por_subject.get(s["id"], [])
    progresso = subject_progress(tarefas_da_disc)
    pct = float(progresso.get("percentage") or 0.0)
    linhas_chart.append({
        "Disciplina": nome,
        "Progresso": pct,
        "Concluídas": progresso.get("completed", 0),
        "Total": progresso.get("total", 0),
    })

if not linhas_chart:
    st.info("Nenhuma disciplina ativa para exibir progresso.")
else:
    df_progress = pd.DataFrame(linhas_chart)
    # Paleta candy pastel — uma cor por disciplina, em ciclo se passar de 8.
    palette = [
        "#A78BFA",  # lavender
        "#F9C5D5",  # pink candy
        "#A7E8DD",  # mint
        "#7C3AED",  # purple
        "#3B82F6",  # blue
        "#EC4899",  # magenta
        "#FCD34D",  # yellow soft
        "#34D399",  # green soft
    ]
    bar = (
        alt.Chart(df_progress)
        .mark_bar(
            cornerRadiusTopRight=6,
            cornerRadiusBottomRight=6,
            cornerRadiusTopLeft=6,
            cornerRadiusBottomLeft=6,
            size=10,
        )
        .encode(
            y=alt.Y(
                "Disciplina:N",
                sort="-x",
                title=None,
                axis=alt.Axis(labelFontSize=13, labelPadding=10),
            ),
            x=alt.X(
                "Progresso:Q",
                title=None,
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(format="d", values=[0, 25, 50, 75, 100], grid=True),
            ),
            color=alt.Color(
                "Disciplina:N",
                scale=alt.Scale(range=palette),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Disciplina:N"),
                alt.Tooltip("Progresso:Q", format=".1f", title="% concluído"),
                alt.Tooltip("Concluídas:Q"),
                alt.Tooltip("Total:Q"),
            ],
        )
    )
    # Texto com o % a direita de cada barra
    text = (
        alt.Chart(df_progress)
        .transform_calculate(label="format(datum.Progresso, '.0f') + '%'")
        .mark_text(
            align="left",
            baseline="middle",
            dx=6,
            fontSize=12,
            fontWeight=600,
            color="#1F1B3D",
        )
        .encode(
            y=alt.Y("Disciplina:N", sort="-x"),
            x=alt.X("Progresso:Q"),
            text=alt.Text("label:N"),
        )
    )
    chart = (bar + text).properties(height=max(120, 38 * len(linhas_chart)))
    st.altair_chart(chart, use_container_width=True)

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
