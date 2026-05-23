"""Utilitarios de agregacao para o Dashboard e indicadores de progresso.

Tudo client-side: recebem listas de tarefas/disciplinas e devolvem numeros.
Sem dependencia de rede, sem efeito colateral.
"""

from __future__ import annotations

import datetime as _dt
import json
from typing import Any

from scripts.calculate_progress import calculate_progress


def _parse_date(value: Any) -> _dt.date | None:
    """Aceita string ISO 'YYYY-MM-DD' (ou ISO completa) e devolve datetime.date."""
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


def is_overdue(task: dict, today: _dt.date | None = None) -> bool:
    """Tarefa atrasada: status != 'done' e due_date < hoje."""
    if task.get("status") == "done":
        return False
    today = today or _dt.date.today()
    d = _parse_date(task.get("due_date"))
    return d is not None and d < today


def is_upcoming(task: dict, today: _dt.date | None = None, days: int = 7) -> bool:
    """Tarefa proxima: status != 'done' e hoje <= due_date <= hoje+days."""
    if task.get("status") == "done":
        return False
    today = today or _dt.date.today()
    d = _parse_date(task.get("due_date"))
    if d is None:
        return False
    return today <= d <= today + _dt.timedelta(days=days)


def subject_progress(tasks: list[dict]) -> dict[str, Any]:
    """Reaproveita scripts/calculate_progress.py e devolve dict parseado.

    Retorno: {"total": int, "completed": int, "percentage": float}
    (Em caso de erro, retorna {"total": 0, "completed": 0, "percentage": 0.0}.)
    """
    try:
        result = json.loads(calculate_progress(tasks))
        if "percentage" in result:
            return result
    except (ValueError, TypeError, json.JSONDecodeError):
        pass
    return {"total": 0, "completed": 0, "percentage": 0.0}


def index_tasks_by_subject(tasks: list[dict]) -> dict[int, list[dict]]:
    """Agrupa tarefas por subject_id para lookups rapidos."""
    result: dict[int, list[dict]] = {}
    for t in tasks:
        sid = t.get("subject_id")
        if sid is None:
            continue
        result.setdefault(sid, []).append(t)
    return result


def upcoming_tasks(
    tasks: list[dict],
    *,
    today: _dt.date | None = None,
    limit: int = 5,
) -> list[dict]:
    """Top N tarefas pendentes ordenadas por due_date asc.

    Tarefas sem due_date sao tratadas como "futuro distante" (vao para o fim).
    """
    today = today or _dt.date.today()
    far_future = _dt.date(9999, 12, 31)

    def _key(t: dict) -> _dt.date:
        d = _parse_date(t.get("due_date"))
        return d if d else far_future

    pendentes = [t for t in tasks if t.get("status") != "done"]
    return sorted(pendentes, key=_key)[:limit]
