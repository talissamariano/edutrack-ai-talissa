# Change: disciplines-frontend-integration-v1

## Why

A página [pages/1_📚_Disciplinas.py](pages/1_📚_Disciplinas.py) é hoje um mockup com dados estáticos. O backend de `subjects` no Xano já tem CRUD completo + endpoint de busca avançada (changes anteriores). Esta change conecta o frontend ao backend para que o aluno autenticado consiga listar, criar, editar, excluir e buscar suas disciplinas usando apenas componentes nativos do Streamlit.

## What Changes

Escopo restrito aos 5 requisitos pedidos + dois ajustes técnicos necessários para a integração funcionar:

1. **Listagem dinâmica** — consumir `GET /subjects` (já existente) e exibir as disciplinas do usuário autenticado em `st.dataframe`/`st.expander`.
2. **Cadastro com validação** — formulário `st.form` para criar disciplina; backend valida duplicado por `(user_id, name, professor)`.
3. **Edição e exclusão** — chamada a `PATCH /subjects/{id}` e `DELETE /subjects/{id}` (já existentes); exclusão exige confirmação via modal nativo (`st.dialog`).
4. **Busca avançada e filtros híbridos** — integrar `GET /subjects/search` (already existente) com filtros por nome **ou** por presença de tarefas em atraso.
5. **Interface Standard** — uso estrito de `st.columns`, `st.tabs`, `st.dataframe`, `st.error`, `st.success`, `st.form`, `st.button`, `st.dialog`. **Sem** `st.markdown(unsafe_allow_html=True)` para estilo.

Ajustes técnicos necessários (pré-requisitos desta change):

- **Schema:** adicionar campo `professor` (text) na tabela `subjects` e atualizar `create_subject`/`update_subject` para aceitá-lo; `create_subject` ganha regra de duplicado por `(user_id, name, professor)`.
- **Helper multi-grupo:** refatorar [lib/xano_client.py](lib/xano_client.py) para suportar URLs base por api_group (hoje só `Authentication`); atualizar `.streamlit/secrets.toml.example`. Sem isso as chamadas a `/subjects/*` falham (canonicals diferentes no Xano).

Fora de escopo: visual/tema (Dark Modern/Poppins — adiado), paginação, ordenação avançada, integração com Tarefas/Perfil, testes automatizados, push/deploy.

## Capabilities

### New Capabilities
- `disciplines-frontend`: Tela Streamlit completa de gestão de disciplinas integrada ao backend Xano via `subjects` CRUD e busca avançada, com regra de duplicado por (user, name, professor) e confirmação nativa de exclusão.

### Modified Capabilities
<!-- Nenhuma capability existente tem requisitos alterados; o campo professor é adição de dado, não muda spec-level behavior das specs subjects-access-control / subjects-search. -->


## Impact

- **Backend Xano:**
  - [tables/837132_subjects.xs](tables/837132_subjects.xs) — campo `professor` (text) adicionado
  - [functions/subjects/310154_create_subject.xs](functions/subjects/310154_create_subject.xs) — input `professor` + validação de duplicado
  - [functions/subjects/310156_update_subject.xs](functions/subjects/310156_update_subject.xs) — input `professor`
- **Helper Streamlit:**
  - [lib/xano_client.py](lib/xano_client.py) — `_request` ganha parâmetro `group`; funções `subjects_list`/`subjects_create`/`subjects_update`/`subjects_delete`/`subjects_search`
  - [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) — novo formato: `xano_auth_base_url` + `xano_subjects_base_url`
- **Frontend:**
  - [pages/1_📚_Disciplinas.py](pages/1_📚_Disciplinas.py) — reescrita integrando ao Xano
- **Sem push/deploy** (AGENTS.md Regra Nº2): a entrega termina na geração dos arquivos; você sobe ao Xano e ajusta o secrets manualmente.
