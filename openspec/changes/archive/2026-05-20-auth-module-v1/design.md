## Context

Auditoria revelou que **a maior parte do backend de auth já existe** (Quick Start do Xano) em `apis/authentication/` com `api_group "Authentication"`, tag `xano:quick-start`:

- `POST /auth/signup` ([3894322_auth_signup_POST.xs](apis/authentication/3894322_auth_signup_POST.xs))
- `POST /auth/login` ([3894320_auth_login_POST.xs](apis/authentication/3894320_auth_login_POST.xs))
- `GET /auth/me` ([3894321_auth_me_GET.xs](apis/authentication/3894321_auth_me_GET.xs))
- `GET /reset/request-reset-link` ([3894326_reset_request_reset_link_GET.xs](apis/authentication/3894326_reset_request_reset_link_GET.xs))
- `POST /reset/magic-link-login` ([3894325_reset_magic_link_login_POST.xs](apis/authentication/3894325_reset_magic_link_login_POST.xs))
- `POST /reset/update_password` ([3894327_reset_update_password_POST.xs](apis/authentication/3894327_reset_update_password_POST.xs))

Frontend Streamlit é um stub básico em [app.py](app.py) + 3 páginas (Disciplinas/Tarefas/Perfil) sem auth. Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

Observação: padrão visual ("Dark Modern" + Poppins) **não existe no AGENTS.md** e foi adiado pelo usuário; este design não cobre UI/tema.

## Goals / Non-Goals

**Goals:**
- Auditar/usar o backend existente sem duplicar.
- Implementar somente o que falta: `PATCH /auth/profile`, sessão Streamlit, logout por expiração.

**Non-Goals:**
- Duplicar signup/login/reset existentes.
- UI/tema/tipografia (adiado).
- Push/sync/deploy.

## Decisions

### Backend Xano

- **Novo endpoint `PATCH /auth/profile`** em `apis/authentication/`, `auth = "user"`, no `api_group "Authentication"`, tag `["edutrack"]`. Atualiza `name` e/ou `email` em `user` filtrando por `id == $auth.id` (nunca de input). Quando `email` for alterado, validar unicidade (`db.get user by email` + `precondition` se outro `id`).
- **Padrão local:** as queries de auth existentes mantêm a lógica direto no `.xs` (sem função separada em `functions/auth/`). Seguir o mesmo padrão no novo endpoint.
- **Sintaxe confirmada nos arquivos existentes:** `db.get`, `db.edit`, `precondition`, `security.create_auth_token`, `security.check_password`, `security.create_uuid`, `util.send_email`, `util.template_engine`, `$auth.id`, `$env.<var>`, `|set`, `|concat`, `|add_secs_to_timestamp`, `|get`, `|to_int`.

### Frontend Streamlit

- **Novo módulo `lib/xano_client.py`:** cliente HTTP central usando `requests` (já em `requirements.txt`).
  - URL base lida via `st.secrets["xano_base_url"]` (fallback para placeholder local com mensagem clara).
  - Funções: `signup`, `login`, `me`, `update_profile`, `request_reset`, `magic_link_login`, `update_password`.
  - Função `_request(method, path, *, auth=False, **kwargs)` injeta `Authorization: Bearer <token>` quando `auth=True`, e em resposta 401/403 limpa `st.session_state["auth_token"]`/`["user"]` e lança `SessionExpired` para a página tratar (item 5).
- **`app.py` ganha gate de autenticação:** se não houver `auth_token`, exibe abas Login/Cadastro; caso contrário, mostra dashboard + sidebar com botão "Sair" (limpa sessão).
- **`pages/3_👤_Perfil.py`:** chama `me()` para exibir o perfil; formulário para editar `name`/`email` chamando `update_profile()`.
- **Persistência cross-reload:** usar cookie de navegador via `extra-streamlit-components.CookieManager` (`COOKIE_NAME = "edutrack_auth_token"`, expiração 86400s alinhada ao token Xano). Helper `restore_session()` chamado no início de `app.py` e de cada página relê o cookie quando `st.session_state` está vazio.
- **Secrets:** `xano_base_url` lido de `st.secrets`; template versionado em `.streamlit/secrets.toml.example`; arquivo real `.streamlit/secrets.toml` ignorado pelo Git.

### Idioma e segurança

- Documentação/comentários de UI em português; nomes técnicos/endpoints em inglês.
- Toda escrita no backend usa `$auth.id` do token; nunca confia em input do cliente para identificar o usuário.

## Risks / Trade-offs

- [Sessão Streamlit cross-reload] → Resolvido com cookie via `extra-streamlit-components` (nova dependência adicionada ao `requirements.txt`); o cookie expira em 86400s alinhado ao token Xano.
- [URL do Xano fora do repo] → Usar `st.secrets` é a forma idiomática; template em `.streamlit/secrets.toml.example`; o helper falha com mensagem clara se ausente.
- [`requirements.txt` estava em UTF-16] → Reescrito como UTF-8 para que `pip install -r` funcione (correção colateral).
- [Mudança de email pode colidir com outro usuário] → Tratado com `precondition` de unicidade no novo endpoint.
- [Tema visual adiado] → Sem cobertura aqui; alinhar quando o padrão for definido.
- [Reset em 3 etapas (magic link)] → Difere do "2 etapas" originalmente assumido; spec atualizada para refletir o fluxo real.
