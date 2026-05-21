## 1. Auditoria do backend existente

- [x] 1.1 Confirmar `POST /auth/signup` existente em `apis/authentication/` (cria user, retorna `{authToken, user_id}`)
- [x] 1.2 Confirmar `POST /auth/login` existente em `apis/authentication/` (valida credenciais, retorna `{authToken, user_id}`)
- [x] 1.3 Confirmar fluxo de reset existente: `GET /reset/request-reset-link`, `POST /reset/magic-link-login`, `POST /reset/update_password`

## 2. Edição de perfil (novo)

- [x] 2.1 Criar `PATCH /auth/profile` em `apis/authentication/` com `auth = "user"`, atualizando `name`/`email` do `$auth.id` com validação de unicidade de e-mail

## 3. Sessão Streamlit

- [x] 3.1 Criar `lib/xano_client.py` com URL base via `st.secrets`, funções `signup/login/me/update_profile/request_reset/magic_link_login/update_password` e injeção de `Authorization` quando autenticado
- [x] 3.2 Persistir `auth_token` e `user` em `st.session_state` após login/signup

## 4. Gate de autenticação na UI

- [x] 4.1 Atualizar `app.py` para exibir abas Login/Cadastro quando não há `auth_token`, e dashboard + botão "Sair" quando autenticado
- [x] 4.2 Atualizar `pages/3_👤_Perfil.py` para exibir o perfil (`me()`) e permitir editar `name`/`email` (`update_profile()`)

## 5. Logout por expiração de token

- [x] 5.1 No helper, detectar resposta `401/403` em chamadas autenticadas, limpar `st.session_state["auth_token"]`/`["user"]` e sinalizar expiração à página
- [x] 5.2 Páginas tratam o sinal de expiração exibindo aviso e voltando à tela de login
