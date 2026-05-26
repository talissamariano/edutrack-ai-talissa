"""Pagina de Perfil: exibe e permite editar nome, e-mail e aniversario.

O gate de autenticacao eh feito pelo roteador (app.py): esta pagina so eh
acessivel apos login. Em caso de token expirar durante o uso, sinalizamos e
o roteador volta para a tela de login no proximo rerun.
"""

import datetime as _dt

import streamlit as st

from lib import xano_client as xano

st.title("👤 Meu Perfil")


def _handle_expiration() -> None:
    st.session_state["_session_expired_notice"] = True
    st.rerun()


def _parse_date(value) -> _dt.date | None:
    if not value:
        return None
    if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
        return value
    text = str(value)[:10]
    try:
        return _dt.date.fromisoformat(text)
    except ValueError:
        return None


def _format_br(d: _dt.date | None) -> str:
    return d.strftime("%d/%m/%Y") if d else "-"


# Carrega o perfil atual via /auth/me
try:
    profile = xano.me()
except xano.SessionExpired:
    _handle_expiration()
    st.stop()
except xano.XanoError as exc:
    st.error(str(exc))
    st.stop()

birthday_atual = _parse_date(profile.get("birthday"))

st.subheader("Dados atuais")
st.write(f"**Nome:** {profile.get('name', '-')}")
st.write(f"**E-mail:** {profile.get('email', '-')}")
st.write(f"**Aniversário:** {_format_br(birthday_atual)}")

st.markdown("---")
st.subheader("Editar perfil")
with st.form("form_profile"):
    new_name = st.text_input("Nome", value=profile.get("name", ""))
    new_email = st.text_input("E-mail", value=profile.get("email", ""))

    informar_aniv = st.toggle(
        "Informar aniversário",
        value=birthday_atual is not None,
        help="Ligue para registrar (ou alterar) sua data de aniversário.",
    )
    new_birthday: _dt.date | None = None
    if informar_aniv:
        new_birthday = st.date_input(
            "Aniversário",
            value=birthday_atual or _dt.date(2000, 1, 1),
            min_value=_dt.date(1900, 1, 1),
            max_value=_dt.date.today(),
            format="DD/MM/YYYY",
        )

    submitted = st.form_submit_button("Salvar", type="primary")

if submitted:
    try:
        # Sempre envia birthday: data ISO se ligado, string vazia se desligado (limpa).
        birthday_payload = new_birthday.isoformat() if informar_aniv and new_birthday else ""
        updated = xano.update_profile(
            name=new_name,
            email=new_email,
            birthday=birthday_payload,
        )
        if isinstance(updated, dict) and "id" in updated:
            st.session_state["user"] = {"id": updated["id"]}
        st.success("Perfil atualizado.")
        st.rerun()
    except xano.SessionExpired:
        _handle_expiration()
    except xano.XanoError as exc:
        st.error(str(exc))
