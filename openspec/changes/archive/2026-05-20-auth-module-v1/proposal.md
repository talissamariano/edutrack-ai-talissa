# Change: auth-module-v1

## Why

O EduTrack AI precisa de um módulo coeso de autenticação e gestão de perfil. O Xano Quick Start já entregou parte do backend (`apis/authentication/`), mas faltam peças (edição de perfil) e o frontend Streamlit ainda não usa autenticação. Esta change **audita o que existe** e **implementa só o que falta**, evitando duplicação.

## What Changes

Escopo estritamente limitado aos 5 itens solicitados:

1. **Cadastro e Login** — auditados; **já existem** em `apis/authentication/` (`POST /auth/signup`, `POST /auth/login`) usando `security.create_auth_token` (expiration 86400s).
2. **Persistência de sessão no Streamlit** — implementar `st.session_state["auth_token"]` e `st.session_state["user"]` após login/signup, com helper central de chamadas ao Xano.
3. **Edição de perfil** — criar `PATCH /auth/profile` (`auth = "user"`) para atualizar `name`/`email` do usuário autenticado (não existe hoje).
4. **Redefinição de senha** — auditada; **já existe** em fluxo de 3 etapas via magic link + e-mail (`GET /reset/request-reset-link`, `POST /reset/magic-link-login`, `POST /reset/update_password`).
5. **Logout por expiração de token** — implementar detecção de resposta não autorizada (token expirado) no helper Streamlit, limpando `st.session_state` e redirecionando ao login.

Fora de escopo: visual/tema (Dark Modern/Poppins — adiados), OAuth, RBAC, envio de e-mail real do reset (já implementado via `util.send_email`), testes automatizados, push/deploy.

## Capabilities

### New Capabilities
- `auth-module`: Cadastro, login, persistência de sessão, edição de perfil, redefinição de senha e logout por expiração de token, sobre a autenticação nativa do Xano.

### Modified Capabilities
<!-- Nenhuma spec permanente existente tem requisitos alterados. -->

## Impact

- **Backend Xano:** novo endpoint `PATCH /auth/profile` em `apis/authentication/` (api_group existente `Authentication`).
- **Frontend Streamlit:** novo módulo `lib/xano_client.py` (helper + detecção de expiração); `app.py` ganha gate de autenticação e logout; `pages/3_👤_Perfil.py` ganha exibição e edição de perfil.
- **Reuso:** signup/login/reset existentes não são alterados.
- **Sem push/deploy:** entrega limitada à geração dos arquivos (AGENTS.md Regra Nº2).
