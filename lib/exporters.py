"""Helpers puros pra exportar dados acadêmicos em CSV e PDF.

Funções não dependem de Streamlit, não fazem I/O em disco, não chamam Xano.
Recebem listas de dicts e retornam `bytes`.
"""

from __future__ import annotations

import csv as _csv
import datetime as _dt
import io as _io
from typing import Any

from fpdf import FPDF

from lib.dashboard_utils import (
    index_tasks_by_subject,
    is_overdue,
    subject_progress,
    upcoming_tasks,
)

_STATUS_LABEL = {"pending": "Pendente", "in_progress": "Em andamento", "done": "Concluída"}
_PRIORITY_LABEL = {"low": "Baixa", "medium": "Média", "high": "Alta"}


def _parse_date(value: Any) -> _dt.date | None:
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


def _fmt_date_br(value: Any) -> str:
    d = _parse_date(value)
    return d.strftime("%d/%m/%Y") if d else "-"


def _fmt_int(value: Any) -> str:
    try:
        n = int(value)
        return str(n) if n > 0 else "-"
    except (TypeError, ValueError):
        return "-"


def _latin1_safe(text: Any) -> str:
    """Sanitiza texto pra latin-1 (fonte Helvetica do fpdf2).

    PT-BR (acentos, ç) cabe em latin-1. Trocamos só os caracteres fora dele
    (em-dash, aspas tipográficas, etc.) por equivalentes ASCII.
    """
    s = str(text) if text is not None else ""
    replacements = {
        "—": "-",   # em dash
        "–": "-",   # en dash
        "‘": "'", "’": "'",  # aspas simples tipográficas
        "“": '"', "”": '"',  # aspas duplas tipográficas
        "…": "...",
        "•": "*",
        " ": " ",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s.encode("latin-1", errors="replace").decode("latin-1")


def _csv_bytes(rows: list[list[Any]]) -> bytes:
    """Serializa linhas em CSV UTF-8 com BOM (abre certinho no Excel pt-BR)."""
    buf = _io.StringIO()
    writer = _csv.writer(buf, lineterminator="\n")
    for r in rows:
        writer.writerow(r)
    return ("﻿" + buf.getvalue()).encode("utf-8")


# -----------------------------------------------------------------------------
# Tarefas
# -----------------------------------------------------------------------------

_TASKS_HEADER = ["Título", "Disciplina", "Prazo", "Status", "Prioridade", "Descrição"]


def _task_row(task: dict, subjects_by_id: dict[int, dict]) -> list[str]:
    subj = subjects_by_id.get(task.get("subject_id")) or {}
    return [
        task.get("title") or "(sem título)",
        subj.get("name") or "-",
        _fmt_date_br(task.get("due_date")),
        _STATUS_LABEL.get(task.get("status"), task.get("status") or "-"),
        _PRIORITY_LABEL.get(task.get("priority"), "Sem prioridade"),
        task.get("description") or "",
    ]


def tasks_to_csv(tasks: list[dict], subjects_by_id: dict[int, dict]) -> bytes:
    rows: list[list[Any]] = [_TASKS_HEADER]
    for t in tasks:
        rows.append(_task_row(t, subjects_by_id))
    return _csv_bytes(rows)


# -----------------------------------------------------------------------------
# Disciplinas
# -----------------------------------------------------------------------------

_SUBJECTS_HEADER = [
    "Nome", "Professor", "Carga horária", "Semestre",
    "Progresso (%)", "Total de tarefas", "Concluídas",
]


def _subject_row(subj: dict, tasks_by_subject: dict[int, list[dict]]) -> list[str]:
    sid = subj.get("id")
    tarefas = tasks_by_subject.get(sid, [])
    prog = subject_progress(tarefas)
    return [
        subj.get("name") or "-",
        subj.get("professor") or "-",
        _fmt_int(subj.get("workload_hours")),
        _fmt_int(subj.get("semester")),
        f"{float(prog.get('percentage') or 0.0):.0f}",
        str(int(prog.get("total") or 0)),
        str(int(prog.get("completed") or 0)),
    ]


def subjects_to_csv(subjects: list[dict], tasks: list[dict]) -> bytes:
    tbs = index_tasks_by_subject(tasks)
    rows: list[list[Any]] = [_SUBJECTS_HEADER]
    for s in subjects:
        rows.append(_subject_row(s, tbs))
    return _csv_bytes(rows)


# -----------------------------------------------------------------------------
# Dashboard snapshot
# -----------------------------------------------------------------------------

def _dashboard_data(
    subjects: list[dict], tasks: list[dict], today: _dt.date
) -> dict[str, Any]:
    ativas = [s for s in subjects if not s.get("archived_at")]
    pendentes = [t for t in tasks if t.get("status") != "done"]
    atrasadas = [t for t in pendentes if is_overdue(t, today)]
    prog_geral = subject_progress(tasks)
    tbs = index_tasks_by_subject(tasks)
    by_disc = []
    for s in ativas:
        prog = subject_progress(tbs.get(s.get("id"), []))
        by_disc.append({
            "name": s.get("name") or "-",
            "percentage": float(prog.get("percentage") or 0.0),
            "completed": int(prog.get("completed") or 0),
            "total": int(prog.get("total") or 0),
        })
    proximas = upcoming_tasks(tasks, today=today, limit=5)
    subj_by_id = {s.get("id"): s for s in subjects if "id" in s}
    proximas_rows = [
        {
            "title": t.get("title") or "(sem título)",
            "subject": (subj_by_id.get(t.get("subject_id")) or {}).get("name") or "-",
            "due_date": _fmt_date_br(t.get("due_date")),
            "overdue": is_overdue(t, today),
        }
        for t in proximas
    ]
    return {
        "metrics": {
            "ativas": len(ativas),
            "pendentes": len(pendentes),
            "atrasadas": len(atrasadas),
            "progresso": float(prog_geral.get("percentage") or 0.0),
        },
        "by_discipline": by_disc,
        "proximas": proximas_rows,
    }


def dashboard_snapshot_to_csv(
    subjects: list[dict], tasks: list[dict], today: _dt.date
) -> bytes:
    data = _dashboard_data(subjects, tasks, today)
    rows: list[list[Any]] = []
    rows.append(["EduTrack AI — Resumo", _fmt_date_br(today)])
    rows.append([])
    rows.append(["Métricas"])
    rows.append(["Disciplinas ativas", data["metrics"]["ativas"]])
    rows.append(["Tarefas pendentes", data["metrics"]["pendentes"]])
    rows.append(["Tarefas atrasadas", data["metrics"]["atrasadas"]])
    rows.append(["Progresso geral (%)", f"{data['metrics']['progresso']:.0f}"])
    rows.append([])
    rows.append(["Progresso por disciplina"])
    rows.append(["Disciplina", "Progresso (%)", "Concluídas", "Total"])
    for d in data["by_discipline"]:
        rows.append([d["name"], f"{d['percentage']:.0f}", d["completed"], d["total"]])
    rows.append([])
    rows.append(["Próximas tarefas"])
    rows.append(["Título", "Disciplina", "Prazo", "Atrasada?"])
    for p in data["proximas"]:
        rows.append([p["title"], p["subject"], p["due_date"], "Sim" if p["overdue"] else "Não"])
    return _csv_bytes(rows)


# -----------------------------------------------------------------------------
# PDF
# -----------------------------------------------------------------------------

class _PDF(FPDF):
    def __init__(self, *, title: str, subtitle: str = "") -> None:
        super().__init__(orientation="P", unit="mm", format="A4")
        self._title_text = title
        self._subtitle_text = subtitle
        self.set_auto_page_break(auto=True, margin=15)

    def header(self) -> None:
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, _latin1_safe(self._title_text), new_x="LMARGIN", new_y="NEXT")
        if self._subtitle_text:
            self.set_font("Helvetica", "", 10)
            self.set_text_color(110, 110, 110)
            self.cell(0, 6, _latin1_safe(self._subtitle_text), new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)
        self.ln(2)

    def footer(self) -> None:
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, _latin1_safe(f"Página {self.page_no()}"), align="C")
        self.set_text_color(0, 0, 0)


def _draw_table(
    pdf: _PDF,
    header: list[str],
    rows: list[list[str]],
    widths: list[float],
) -> None:
    line_h = 6
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(243, 238, 254)
    for i, h in enumerate(header):
        pdf.cell(widths[i], line_h, _latin1_safe(h), border=1, fill=True)
    pdf.ln(line_h)
    pdf.set_font("Helvetica", "", 9)
    for row in rows:
        safe_row = [_latin1_safe(cell) for cell in row]
        cell_lines = [pdf.multi_cell(widths[i], line_h, safe_row[i],
                                     border=0, dry_run=True, output="LINES")
                      for i in range(len(safe_row))]
        max_lines = max((len(c) for c in cell_lines), default=1)
        row_h = line_h * max_lines
        if pdf.get_y() + row_h > pdf.h - pdf.b_margin:
            pdf.add_page()
        x0, y0 = pdf.get_x(), pdf.get_y()
        for i, cell in enumerate(safe_row):
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.multi_cell(widths[i], line_h, cell, border=1, align="L")
            pdf.set_xy(x + widths[i], y)
        pdf.set_xy(x0, y0 + row_h)


def _pdf_bytes(pdf: _PDF) -> bytes:
    out = pdf.output()
    return bytes(out) if isinstance(out, bytearray) else out


def tasks_to_pdf(
    tasks: list[dict],
    subjects_by_id: dict[int, dict],
    *,
    title: str = "EduTrack AI — Tarefas",
) -> bytes:
    today = _dt.date.today()
    pdf = _PDF(title=title, subtitle=f"Gerado em {today.strftime('%d/%m/%Y')}")
    pdf.add_page()
    if not tasks:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, _latin1_safe("Nenhuma tarefa para listar."))
        return _pdf_bytes(pdf)
    rows = [_task_row(t, subjects_by_id) for t in tasks]
    widths = [42, 32, 22, 24, 22, 38]
    _draw_table(pdf, _TASKS_HEADER, rows, widths)
    return _pdf_bytes(pdf)


def subjects_to_pdf(
    subjects: list[dict],
    tasks: list[dict],
    *,
    title: str = "EduTrack AI — Disciplinas",
) -> bytes:
    today = _dt.date.today()
    pdf = _PDF(title=title, subtitle=f"Gerado em {today.strftime('%d/%m/%Y')}")
    pdf.add_page()
    if not subjects:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, _latin1_safe("Nenhuma disciplina cadastrada."))
        return _pdf_bytes(pdf)
    tbs = index_tasks_by_subject(tasks)
    rows = [_subject_row(s, tbs) for s in subjects]
    widths = [44, 36, 22, 18, 24, 22, 22]
    _draw_table(pdf, _SUBJECTS_HEADER, rows, widths)
    return _pdf_bytes(pdf)


def dashboard_snapshot_to_pdf(
    subjects: list[dict],
    tasks: list[dict],
    today: _dt.date,
) -> bytes:
    data = _dashboard_data(subjects, tasks, today)
    pdf = _PDF(
        title="EduTrack AI — Resumo",
        subtitle=f"Gerado em {today.strftime('%d/%m/%Y')}",
    )
    pdf.add_page()

    def _txt(s: str) -> str:
        return _latin1_safe(s)

    # Métricas
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, _txt("Métricas"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    m = data["metrics"]
    for label, val in [
        ("Disciplinas ativas", m["ativas"]),
        ("Tarefas pendentes", m["pendentes"]),
        ("Tarefas atrasadas", m["atrasadas"]),
        ("Progresso geral", f"{m['progresso']:.0f}%"),
    ]:
        pdf.cell(60, 6, _txt(f"{label}:"))
        pdf.cell(0, 6, _txt(str(val)), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, _txt("Progresso por disciplina"), new_x="LMARGIN", new_y="NEXT")
    if data["by_discipline"]:
        rows = [
            [d["name"], f"{d['percentage']:.0f}%", str(d["completed"]), str(d["total"])]
            for d in data["by_discipline"]
        ]
        _draw_table(
            pdf,
            ["Disciplina", "Progresso", "Concluídas", "Total"],
            rows,
            [80, 30, 30, 30],
        )
    else:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 6, _txt("Nenhuma disciplina ativa."), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, _txt("Próximas tarefas"), new_x="LMARGIN", new_y="NEXT")
    if data["proximas"]:
        rows = [
            [p["title"], p["subject"], p["due_date"], "Sim" if p["overdue"] else "Não"]
            for p in data["proximas"]
        ]
        _draw_table(
            pdf,
            ["Título", "Disciplina", "Prazo", "Atrasada?"],
            rows,
            [60, 60, 30, 22],
        )
    else:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 6, _txt("Nenhuma tarefa pendente."), new_x="LMARGIN", new_y="NEXT")

    return _pdf_bytes(pdf)
