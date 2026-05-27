# auth-module Specification (delta)

## MODIFIED Requirements

### Requirement: Tela de login/cadastro

O frontend Streamlit SHALL exibir a tela de autenticação com layout em duas colunas: coluna esquerda com identidade visual do app (título, slogan, destaques de funcionalidades) e coluna direita com os formulários de login, cadastro e recuperação de senha em tabs. O layout SHALL usar exclusivamente componentes nativos do Streamlit sem `unsafe_allow_html=True`.

#### Scenario: Visualização da tela de login

- **WHEN** o usuário não autenticado acessa o app
- **THEN** a tela exibe duas colunas: à esquerda o nome/logo do app com slogan e destaques; à direita as tabs "Entrar", "Cadastrar" e "Esqueci a senha"

#### Scenario: Funcionalidade preservada

- **WHEN** o usuário preenche e submete qualquer formulário (login, cadastro ou reset)
- **THEN** o comportamento de autenticação permanece idêntico ao anterior (chama os mesmos endpoints Xano, armazena sessão da mesma forma)

#### Scenario: Inspeção do código

- **WHEN** o código de `login.py` é inspecionado
- **THEN** não há chamadas a `unsafe_allow_html=True` com HTML/CSS para estilo
