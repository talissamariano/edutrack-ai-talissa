# auth-module Specification

## Purpose

Define os fluxos de autenticação e gestão de perfil do EduTrack AI sobre a autenticação nativa do Xano: cadastro, login, persistência de sessão Streamlit, edição de perfil, redefinição de senha e logout por expiração de token.

## Requirements

### Requirement: Cadastro de conta

O sistema SHALL permitir criar uma conta com `name`, `email` e `password`, rejeitando e-mail já cadastrado, e retornar um token de autenticação.

#### Scenario: Cadastro bem-sucedido

- **WHEN** um visitante envia `name`, `email` e `password` válidos e o e-mail ainda não existe
- **THEN** o sistema cria o usuário e retorna `{authToken, user_id}`

#### Scenario: E-mail já cadastrado

- **WHEN** o e-mail informado já pertence a um usuário
- **THEN** o sistema rejeita o cadastro com erro e não cria duplicata

### Requirement: Login

O sistema SHALL autenticar um usuário por `email` e `password`, retornando um token de autenticação.

#### Scenario: Login válido

- **WHEN** o usuário envia `email` e `password` corretos
- **THEN** o sistema retorna `{authToken, user_id}`

#### Scenario: Credenciais inválidas

- **WHEN** o `email` não existe ou a `password` está incorreta
- **THEN** o sistema rejeita o login com erro de não autorizado

### Requirement: Persistência de sessão no Streamlit

O frontend Streamlit SHALL armazenar o token de autenticação e o usuário em `st.session_state` após login/signup, mantendo a sessão entre interações.

#### Scenario: Sessão mantida entre interações

- **WHEN** o usuário autentica e em seguida navega entre páginas
- **THEN** o token permanece em `st.session_state` e o usuário continua autenticado sem novo login

#### Scenario: Acesso sem token redireciona ao login

- **WHEN** o usuário acessa qualquer página sem token em `st.session_state`
- **THEN** o Streamlit exibe a tela de login/cadastro e bloqueia o conteúdo

### Requirement: Edição de perfil

O sistema SHALL expor `PATCH /auth/profile` (`auth = "user"`) que permite ao usuário autenticado atualizar `name` e/ou `email`, restrito ao próprio registro (`user_id` do token).

#### Scenario: Atualização de perfil bem-sucedida

- **WHEN** um usuário autenticado envia novo `name` e/ou `email` válidos via `PATCH /auth/profile`
- **THEN** o sistema atualiza o registro do próprio usuário e retorna o perfil atualizado

#### Scenario: Edição sem autenticação

- **WHEN** a requisição a `PATCH /auth/profile` não possui token válido
- **THEN** o sistema rejeita a requisição como não autorizada

### Requirement: Redefinição de senha em fluxo de magic link

O sistema SHALL oferecer um fluxo de redefinição de senha em três etapas via magic link e-mailado: solicitação do link, login com o magic token, e atualização da senha pelo usuário autenticado pelo magic link.

#### Scenario: Solicitação de redefinição

- **WHEN** o usuário solicita redefinição informando um e-mail existente
- **THEN** o sistema gera um token de reset com expiração, atualiza `password_reset` do usuário e envia o magic link por e-mail

#### Scenario: Login com magic token válido

- **WHEN** o usuário envia um `magic_token` válido (não expirado, não usado) e o e-mail correspondente
- **THEN** o sistema retorna um token de autenticação e marca o `password_reset.used` como verdadeiro

#### Scenario: Atualização de senha após magic-link login

- **WHEN** o usuário autenticado via magic link envia `password` e `confirm_password` iguais
- **THEN** o sistema atualiza a senha do próprio usuário

### Requirement: Aniversário no perfil do usuário

O sistema SHALL permitir que o usuário autenticado registre opcionalmente sua data de aniversário (`birthday`), persistida na tabela `user` como `date birthday?`. Os endpoints `GET /auth/me` e `PATCH /auth/profile` SHALL contemplar esse campo (retornar e aceitar atualizar, respectivamente).

#### Scenario: Cadastrar aniversário pela primeira vez

- **WHEN** o usuário autenticado preenche o campo de aniversário no perfil e salva
- **THEN** o sistema persiste a data em `user.birthday` via `PATCH /auth/profile`

#### Scenario: Editar aniversário existente

- **WHEN** o usuário altera o aniversário e salva
- **THEN** o sistema atualiza `user.birthday` para o novo valor

#### Scenario: Sem aniversário cadastrado

- **WHEN** o usuário nunca cadastrou aniversário (campo nulo) e abre o perfil
- **THEN** o campo aparece vazio e o sistema não exibe nenhuma mensagem relacionada na Home

### Requirement: Logout por expiração de token

O frontend Streamlit SHALL detectar respostas de não autorizado por token expirado/inválido nas chamadas ao Xano, limpar `st.session_state` e exibir a tela de login.

#### Scenario: Token expirado durante uso

- **WHEN** uma chamada autenticada retorna erro de não autorizado por token expirado/inválido
- **THEN** o Streamlit limpa `auth_token` e `user` de `st.session_state` e exibe a tela de login
