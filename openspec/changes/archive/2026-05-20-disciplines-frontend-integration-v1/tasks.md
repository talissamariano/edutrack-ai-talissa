## 1. Schema e funções Xano

- [x] 1.1 Adicionar `text professor?` (filters=trim) ao schema da tabela `subjects` em `tables/837132_subjects.xs`
- [x] 1.2 Atualizar `functions/subjects/310154_create_subject.xs` para aceitar `text professor` no input e gravar no `db.add.data`
- [x] 1.3 Adicionar em `create_subject` validação de duplicado: `db.query subjects where user_id==$auth.id && name==$input.name && professor==$input.professor` + `precondition` rejeitando quando já existe
- [x] 1.4 Atualizar `functions/subjects/310156_update_subject.xs` para aceitar `text professor` no input e incluir no `db.edit.data`

## 2. Helper Streamlit multi-grupo

- [x] 2.1 Atualizar `.streamlit/secrets.toml.example` com `xano_auth_base_url` e `xano_subjects_base_url`
- [x] 2.2 Refatorar `_request` em `lib/xano_client.py` para receber `group` (`"auth"` ou `"subjects"`) e resolver a base URL via `_base_url(group)`
- [x] 2.3 Atualizar funções existentes (`signup`, `login`, `me`, `update_profile`, `request_reset`, `magic_link_login`, `update_password`) para passarem `group="auth"`
- [x] 2.4 Adicionar funções `subjects_list`, `subjects_search(name=None, only_overdue=None)`, `subjects_create(name, professor, description)`, `subjects_update(id, *, name=None, professor=None, description=None)`, `subjects_delete(id)`

## 3. Tela de Disciplinas

- [x] 3.1 Reescrever `pages/1_📚_Disciplinas.py` com barra de busca + filtro "atrasadas" no topo, chamando `subjects_search`
- [x] 3.2 Aba "Listar": `st.dataframe` com as disciplinas; `st.expander` por item com botões Editar/Excluir
- [x] 3.3 Aba "Nova Disciplina": `st.form` com `name`, `professor`, `description`; submit chama `subjects_create` e trata duplicado via `st.error`
- [x] 3.4 Edição via `@st.dialog` com form populado chamando `subjects_update`
- [x] 3.5 Exclusão via `@st.dialog` de confirmação com botões Confirmar/Cancelar chamando `subjects_delete`
- [x] 3.6 Tratar `xano.SessionExpired` em todas as chamadas, sinalizando expiração e retornando ao login
- [x] 3.7 Verificar que a tela usa apenas componentes Standard (sem `unsafe_allow_html` para estilo)
