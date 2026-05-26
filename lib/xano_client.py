"""Cliente HTTP centralizado para chamadas ao backend Xano.

Suporta multiplos api_groups (cada grupo tem URL base propria, configurada em
.streamlit/secrets.toml). Mantem o token em st.session_state + cookie, injeta
Authorization nas chamadas autenticadas e trata expiracao (401/403) limpando
a sessao.
"""

from __future__ import annotations

import datetime as _dt
from typing import Any

import extra_streamlit_components as stx
import requests
import streamlit as st


COOKIE_NAME = "edutrack_auth_token"
TOKEN_TTL_SECONDS = 86400  # alinhado a expiration do Xano (security.create_auth_token)

# Mapeamento group -> chave em st.secrets
_SECRET_KEY_BY_GROUP = {
    "auth": "xano_auth_base_url",
    "subjects": "xano_subjects_base_url",
    "academic_tasks": "xano_academic_tasks_base_url",
}


class SessionExpired(Exception):
    """Sinalizado quando o backend retorna 401/403 em chamada autenticada."""


class XanoError(Exception):
    """Erro generico vindo do backend Xano (status >= 400 nao tratado)."""


_COOKIE_MGR_KEY = "_edutrack_cookie_mgr"


def _cookie_manager() -> stx.CookieManager:
    """CookieManager memoizado em st.session_state (nao usa cache_resource)."""
    mgr = st.session_state.get(_COOKIE_MGR_KEY)
    if mgr is None:
        mgr = stx.CookieManager(key="edutrack_cookie_manager")
        st.session_state[_COOKIE_MGR_KEY] = mgr
    return mgr


def _base_url(group: str) -> str:
    """Le a URL base do api_group em st.secrets.

    Configure em .streamlit/secrets.toml:
        xano_auth_base_url = "https://<inst>.xano.io/api:<auth-canonical>"
        xano_subjects_base_url = "https://<inst>.xano.io/api:<subjects-canonical>"
    """
    secret_key = _SECRET_KEY_BY_GROUP.get(group)
    if secret_key is None:
        raise XanoError(f"Group desconhecido: {group!r}.")
    try:
        return st.secrets[secret_key].rstrip("/")
    except (KeyError, FileNotFoundError, AttributeError) as exc:
        raise XanoError(
            f"{secret_key} nao configurado. Defina em .streamlit/secrets.toml."
        ) from exc


def _request(
    method: str,
    path: str,
    *,
    group: str,
    auth: bool = False,
    json: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> Any:
    """Executa a requisicao no api_group informado e trata expiracao."""
    headers: dict[str, str] = {}
    if auth:
        token = st.session_state.get("auth_token")
        if not token:
            raise SessionExpired("Sem token na sessao.")
        headers["Authorization"] = f"Bearer {token}"

    url = f"{_base_url(group)}{path}"
    try:
        response = requests.request(
            method, url, headers=headers, json=json, params=params, timeout=15
        )
    except requests.RequestException as exc:
        raise XanoError(f"Falha de rede ao chamar {path}: {exc}") from exc

    # Token genuinamente invalido/expirado -> limpa sessao + cookie.
    # 403 (accessdenied) significa "token valido mas acao proibida" (ex.: duplicado,
    # ownership) e NAO deve deslogar o usuario; vira XanoError normal abaixo.
    if auth and response.status_code == 401:
        clear_session()
        raise SessionExpired("Token expirado ou invalido.")

    if response.status_code >= 400:
        try:
            payload = response.json()
            message = payload.get("message") or payload.get("error") or response.text
        except ValueError:
            message = response.text
        raise XanoError(f"{response.status_code}: {message}")

    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


# ---------------------------------------------------------------------------
# Auth (api_group "Authentication")
# ---------------------------------------------------------------------------

def signup(name: str, email: str, password: str) -> dict[str, Any]:
    return _request(
        "POST",
        "/auth/signup",
        group="auth",
        json={"name": name, "email": email, "password": password},
    )


def login(email: str, password: str) -> dict[str, Any]:
    return _request(
        "POST",
        "/auth/login",
        group="auth",
        json={"email": email, "password": password},
    )


def me() -> dict[str, Any]:
    return _request("GET", "/auth/me", group="auth", auth=True)


def update_profile(
    *,
    name: str | None = None,
    email: str | None = None,
    birthday: str | None = None,
) -> dict[str, Any]:
    """PATCH /auth/profile -> atualiza nome, email e/ou aniversario.

    birthday: string ISO 'YYYY-MM-DD' para gravar uma data, ou None para nao alterar.
    Para limpar o aniversario, passar string vazia "".
    """
    payload: dict[str, Any] = {}
    if name is not None:
        payload["name"] = name
    if email is not None:
        payload["email"] = email
    if birthday is not None:
        payload["birthday"] = birthday
    return _request("PATCH", "/auth/profile", group="auth", auth=True, json=payload)


def request_reset(email: str) -> dict[str, Any]:
    return _request(
        "GET", "/reset/request-reset-link", group="auth", params={"email": email}
    )


def magic_link_login(magic_token: str, email: str) -> dict[str, Any]:
    return _request(
        "POST",
        "/reset/magic-link-login",
        group="auth",
        json={"magic_token": magic_token, "email": email},
    )


def update_password(password: str, confirm_password: str) -> dict[str, Any]:
    return _request(
        "POST",
        "/reset/update_password",
        group="auth",
        auth=True,
        json={"password": password, "confirm_password": confirm_password},
    )


# ---------------------------------------------------------------------------
# Subjects (api_group "subjects")
# ---------------------------------------------------------------------------

def subjects_list() -> list[dict[str, Any]]:
    """GET /subjects -> lista de disciplinas do usuario autenticado."""
    return _request("GET", "/subjects", group="subjects", auth=True) or []


def subjects_search(
    *, name: str | None = None, only_overdue: bool | None = None
) -> list[dict[str, Any]]:
    """GET /subjects/search -> filtra por nome OU por tarefas atrasadas."""
    params: dict[str, Any] = {}
    if name:
        params["name"] = name
    if only_overdue:
        params["only_overdue"] = "true"
    return _request(
        "GET", "/subjects/search", group="subjects", auth=True, params=params
    ) or []


def subjects_create(
    name: str,
    professor: str,
    description: str = "",
    *,
    workload_hours: int | None = None,
    semester: int | None = None,
) -> dict[str, Any]:
    """POST /subjects -> cria disciplina vinculada ao usuario autenticado.

    Campos opcionais (description, workload_hours, semester) sao omitidos
    do payload quando vazios/None, alinhado ao backend.
    """
    payload: dict[str, Any] = {"name": name, "professor": professor}
    if description:
        payload["description"] = description
    if workload_hours is not None:
        payload["workload_hours"] = workload_hours
    if semester is not None:
        payload["semester"] = semester
    return _request("POST", "/subjects", group="subjects", auth=True, json=payload)


def subjects_update(
    subject_id: int,
    *,
    name: str | None = None,
    professor: str | None = None,
    description: str | None = None,
    workload_hours: int | None = None,
    semester: int | None = None,
) -> dict[str, Any]:
    """PATCH /subjects/{id} -> atualiza disciplina do proprio usuario."""
    payload: dict[str, Any] = {}
    if name is not None:
        payload["name"] = name
    if professor is not None:
        payload["professor"] = professor
    # description so vai se for string nao vazia; backend aceita ausencia (opcional)
    if description:
        payload["description"] = description
    if workload_hours is not None:
        payload["workload_hours"] = workload_hours
    if semester is not None:
        payload["semester"] = semester
    return _request(
        "PATCH",
        f"/subjects/{subject_id}",
        group="subjects",
        auth=True,
        json=payload,
    )


def subjects_delete(subject_id: int) -> dict[str, Any]:
    """DELETE /subjects/{id} -> remove disciplina do proprio usuario."""
    return _request(
        "DELETE", f"/subjects/{subject_id}", group="subjects", auth=True
    )


def subjects_archive(subject_id: int) -> dict[str, Any]:
    """POST /subjects/{id}/archive -> arquiva a disciplina."""
    return _request(
        "POST",
        f"/subjects/{subject_id}/archive",
        group="subjects",
        auth=True,
        json={"id": subject_id},
    )


def subjects_unarchive(subject_id: int) -> dict[str, Any]:
    """POST /subjects/{id}/unarchive -> reativa a disciplina."""
    return _request(
        "POST",
        f"/subjects/{subject_id}/unarchive",
        group="subjects",
        auth=True,
        json={"id": subject_id},
    )


# ---------------------------------------------------------------------------
# Academic Tasks (api_group "academic_tasks")
# ---------------------------------------------------------------------------

def tasks_list(
    *,
    subject_id: int | None = None,
    status: str | None = None,
    only_overdue: bool | None = None,
    priority: str | None = None,
) -> list[dict[str, Any]]:
    """GET /academic_tasks -> lista as tarefas do usuario autenticado.

    priority eh enviado como param para o backend (que pode ignora-lo);
    o filtro final eh feito client-side em pages/2_Tarefas.py.
    """
    params: dict[str, Any] = {}
    if subject_id is not None:
        params["subject_id"] = subject_id
    if status:
        params["status"] = status
    if only_overdue:
        params["only_overdue"] = "true"
    if priority:
        params["priority"] = priority
    return _request(
        "GET", "/academic_tasks", group="academic_tasks", auth=True, params=params
    ) or []


def tasks_create(
    title: str,
    *,
    subject_id: int,
    status: str = "pending",
    description: str | None = None,
    due_date: str | None = None,
    priority: str | None = None,
) -> dict[str, Any]:
    """POST /academic_tasks -> cria tarefa vinculada ao usuario autenticado.

    due_date deve ser uma string ISO (YYYY-MM-DD) ou None.
    priority: 'low' / 'medium' / 'high' (ou None).
    """
    payload: dict[str, Any] = {
        "title": title,
        "subject_id": subject_id,
        "status": status,
    }
    if description:
        payload["description"] = description
    if due_date:
        payload["due_date"] = due_date
    if priority:
        payload["priority"] = priority
    return _request(
        "POST", "/academic_tasks", group="academic_tasks", auth=True, json=payload
    )


def tasks_update(
    task_id: int,
    *,
    title: str | None = None,
    description: str | None = None,
    due_date: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    subject_id: int | None = None,
) -> dict[str, Any]:
    """PATCH /academic_tasks/{id} -> atualiza a tarefa do proprio usuario."""
    payload: dict[str, Any] = {}
    if title is not None:
        payload["title"] = title
    if description is not None and description != "":
        payload["description"] = description
    if due_date is not None and due_date != "":
        payload["due_date"] = due_date
    if status is not None:
        payload["status"] = status
    if priority is not None:
        payload["priority"] = priority
    if subject_id is not None:
        payload["subject_id"] = subject_id
    return _request(
        "PATCH",
        f"/academic_tasks/{task_id}",
        group="academic_tasks",
        auth=True,
        json=payload,
    )


def tasks_delete(task_id: int) -> dict[str, Any]:
    """DELETE /academic_tasks/{id} -> remove a tarefa do proprio usuario."""
    return _request(
        "DELETE",
        f"/academic_tasks/{task_id}",
        group="academic_tasks",
        auth=True,
    )


def tasks_complete(task_id: int) -> dict[str, Any]:
    """POST /academic_tasks/{id}/complete -> marca a tarefa como done."""
    return _request(
        "POST",
        f"/academic_tasks/{task_id}/complete",
        group="academic_tasks",
        auth=True,
        json={"id": task_id},
    )


# ---------------------------------------------------------------------------
# Sessao Streamlit
# ---------------------------------------------------------------------------

def store_session(auth_payload: dict[str, Any]) -> None:
    """Guarda authToken em st.session_state e em cookie para sobreviver a reloads."""
    token = auth_payload.get("authToken")
    st.session_state["auth_token"] = token
    user_id = auth_payload.get("user_id")
    if user_id is not None:
        st.session_state["user"] = {"id": user_id}

    if token:
        expires_at = _dt.datetime.utcnow() + _dt.timedelta(seconds=TOKEN_TTL_SECONDS)
        try:
            _cookie_manager().set(COOKIE_NAME, token, expires_at=expires_at)
        except Exception:
            # Ambiente sem cookies disponiveis: segue funcional na sessao.
            pass


def clear_session() -> None:
    """Logout local: remove token/usuario da sessao e do cookie."""
    st.session_state.pop("auth_token", None)
    st.session_state.pop("user", None)
    try:
        _cookie_manager().delete(COOKIE_NAME)
    except Exception:
        pass


def restore_session() -> None:
    """Restaura o token a partir do cookie se ainda nao houver na sessao."""
    if st.session_state.get("auth_token"):
        return
    try:
        cookies = _cookie_manager().get_all()
    except Exception:
        return
    if not cookies:
        return
    token = cookies.get(COOKIE_NAME)
    if token:
        st.session_state["auth_token"] = token


def is_authenticated() -> bool:
    return bool(st.session_state.get("auth_token"))
