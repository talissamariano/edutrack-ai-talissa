# disciplines-frontend Specification

## Purpose

Define o comportamento da tela Streamlit de gestão de disciplinas, integrada ao backend Xano para listar, cadastrar, editar, excluir e buscar `subjects` do usuário autenticado, usando exclusivamente componentes nativos do Streamlit.

## ADDED Requirements

### Requirement: Listagem dinâmica vinculada ao usuário autenticado

A tela SHALL listar apenas as disciplinas cujo `user_id` corresponde ao usuário autenticado, consumindo o backend Xano (`GET /subjects` ou `GET /subjects/search`).

#### Scenario: Usuário autenticado abre a página

- **WHEN** um usuário autenticado abre a página de Disciplinas
- **THEN** a tela exibe as suas disciplinas vindas do Xano, incluindo nome, professor e descrição

#### Scenario: Sem sessão válida

- **WHEN** o token está ausente ou expirado ao chamar o backend
- **THEN** a tela sinaliza expiração e o roteador retorna à tela de login

### Requirement: Cadastro com validação de duplicado

A tela SHALL oferecer um formulário (`st.form`) para criar uma disciplina e o backend SHALL rejeitar o cadastro quando já existir disciplina do mesmo usuário com igual `name` e `professor`.

#### Scenario: Cadastro válido

- **WHEN** o usuário submete `name`, `professor` e `description` válidos sem conflito de duplicado
- **THEN** a disciplina é criada no Xano vinculada ao `user_id` autenticado e a tela exibe mensagem de sucesso

#### Scenario: Duplicado detectado

- **WHEN** o usuário submete uma disciplina cujo `(name, professor)` já existe para ele
- **THEN** o backend rejeita com erro e a tela exibe `st.error` com a mensagem

### Requirement: Edição e exclusão com confirmação

A tela SHALL permitir editar (PATCH) e excluir (DELETE) disciplinas do usuário autenticado, e a exclusão SHALL exigir confirmação explícita do usuário antes de chamar o backend.

#### Scenario: Edição bem-sucedida

- **WHEN** o usuário edita uma disciplina e submete o formulário de edição
- **THEN** o sistema envia `PATCH /subjects/{id}` e a lista é atualizada

#### Scenario: Exclusão exige confirmação

- **WHEN** o usuário clica em excluir uma disciplina
- **THEN** a tela abre um diálogo de confirmação nativo (`st.dialog`) com botões "Confirmar" e "Cancelar"

#### Scenario: Confirmação confirma a exclusão

- **WHEN** o usuário clica "Confirmar" no diálogo de exclusão
- **THEN** o sistema envia `DELETE /subjects/{id}` e remove o item da lista

#### Scenario: Cancelar aborta a exclusão

- **WHEN** o usuário clica "Cancelar" no diálogo
- **THEN** nenhuma chamada é feita ao backend e a lista permanece inalterada

### Requirement: Busca avançada e filtros híbridos

A tela SHALL expor um campo de busca por nome e um filtro de "apenas com tarefas atrasadas", consumindo `GET /subjects/search` e combinando os filtros conforme o backend (OU lógico quando ambos forem fornecidos).

#### Scenario: Busca por nome

- **WHEN** o usuário digita um termo no campo de nome e aciona a busca
- **THEN** a lista exibe apenas as disciplinas do usuário cujo `name` corresponde ao termo

#### Scenario: Filtro por tarefas atrasadas

- **WHEN** o usuário ativa o filtro "apenas com tarefas atrasadas"
- **THEN** a lista exibe apenas as disciplinas do usuário com pelo menos uma tarefa atrasada

#### Scenario: Combinação por OU

- **WHEN** o usuário informa termo de nome e também ativa o filtro de atrasadas
- **THEN** a lista exibe disciplinas que correspondem ao nome OU que possuem tarefas atrasadas

### Requirement: Interface Standard sem CSS customizado

A tela SHALL usar exclusivamente componentes nativos do Streamlit: `st.columns`, `st.tabs`, `st.dataframe`, `st.error`, `st.success`, `st.form`, `st.button`, `st.dialog`, `st.expander`, `st.text_input`, `st.checkbox`. Não SHALL utilizar `st.markdown(unsafe_allow_html=True)` para fins de estilização.

#### Scenario: Inspeção do código da página

- **WHEN** o código da página Disciplinas é inspecionado
- **THEN** não há chamadas a `st.markdown(..., unsafe_allow_html=True)` com tags HTML/CSS, nem `<style>` injetado
