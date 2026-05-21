## Context

Backend Xano com `subjects` CRUD + search já implementados em changes anteriores ([apis/subjects/](apis/subjects/), [functions/subjects/](functions/subjects/)). Auth-module-v1 entregou sessão Streamlit com cookie e helper [lib/xano_client.py](lib/xano_client.py) usando **uma única URL base** apontando para o grupo `Authentication` (canonical `8p5JoSuG`). A tela [pages/1_📚_Disciplinas.py](pages/1_📚_Disciplinas.py) é hoje mockup. Streamlit em uso é 1.57 (suporta `st.dialog`). Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Tela Streamlit funcional ponta a ponta para `subjects` (list/create/update/delete/search) com confirmação nativa de exclusão.
- Schema `subjects` ganha `professor`; backend valida duplicado por `(user_id, name, professor)`.
- Helper aceita múltiplos `api_group`.

**Non-Goals:**
- Visual/tema (Dark Modern/Poppins — adiado).
- Paginação, ordenação avançada, importação em massa.
- Integração com Tarefas/Perfil; testes automatizados.
- Push/sync/deploy.

## Decisions

### Backend Xano

- **Tabela `subjects`** ganha `text professor?` (opcional para preservar registros pré-existentes). Filters `trim` para consistência com `name`.
- **`create_subject`** recebe novo input `text professor` e antes do `db.add` faz `db.query subjects { where = user_id == $auth.id && name == $input.name && professor == $input.professor }` → `precondition ($existing == null)` com `error_type = "accessdenied"` e mensagem clara. Grava `professor` no `db.add`.
- **`update_subject`** recebe `text professor` opcional e inclui no `db.edit.data`.
- **`search_subjects`** não muda — já filtra por nome/overdue; o campo `professor` aparece naturalmente na resposta porque o `db.query` retorna o registro completo.
- **`delete_subject` / archive / unarchive** não mudam.
- **Sintaxe XanoScript:** uso apenas operadores já validados em produção (`==`, `&&`, `db.query`, `db.add`, `db.edit`, `precondition`).

### Helper Streamlit (`lib/xano_client.py`)

- **Secrets reformatados** para múltiplos grupos:
  ```toml
  xano_auth_base_url = "https://x8ki-letl-twmt.n7.xano.io/api:8p5JoSuG"
  xano_subjects_base_url = "https://x8ki-letl-twmt.n7.xano.io/api:_7wK5hPz"
  ```
  Formato cópia-e-cola direto do dashboard Xano. Migração: o nome antigo `xano_base_url` deixa de ser usado.
- **`_request(method, path, *, group, ...)`** ganha o parâmetro `group` (string `"auth"` ou `"subjects"`); resolve a base URL via `_base_url(group)` que lê o secret correspondente.
- **Novas funções públicas:** `subjects_list()`, `subjects_search(name=None, only_overdue=None)`, `subjects_create(name, professor, description)`, `subjects_update(id, *, name=None, professor=None, description=None)`, `subjects_delete(id)`.
- **Compatibilidade:** funções existentes (`signup`, `login`, `me`, `update_profile`, `request_reset`, etc.) continuam passando `group="auth"` por dentro; assinaturas externas não mudam.

### Frontend (`pages/1_📚_Disciplinas.py`)

- Layout em `st.tabs`: **"📋 Listar"**, **"➕ Nova Disciplina"**.
- **Barra de busca/filtros** acima das tabs: `st.text_input` para nome + `st.checkbox` "Apenas com tarefas atrasadas" + botão "Buscar". Default = sem filtros (lista tudo).
- **Listagem:** chama `xano.subjects_search(name=..., only_overdue=...)`; resultado renderizado em `st.dataframe` (visão tabular). Abaixo, um `st.expander` por disciplina com botões **Editar** e **Excluir**.
- **Editar:** abre `@st.dialog` com `st.form` populado (`name`, `professor`, `description`) → submit chama `subjects_update`.
- **Excluir:** abre `@st.dialog` com texto de confirmação + dois botões (`Confirmar` chama `subjects_delete`, `Cancelar` fecha sem ação).
- **Nova Disciplina:** `st.form` com `name` (obrigatório), `professor` (obrigatório), `description` (opcional). Submit chama `subjects_create`. Em caso de duplicado, o erro do backend aparece em `st.error`.
- **Tratamento de expiração:** captura `xano.SessionExpired` em qualquer chamada → seta `_session_expired_notice` em `st.session_state` e `st.rerun()` (router cai pro login com aviso).
- **Standard estrito:** zero `unsafe_allow_html` para estilo. Permitido apenas para conteúdo plain markdown.

### Idioma e segurança

- Documentação/UI em português; nomes técnicos/endpoints em inglês.
- Filtro por `user_id` continua sendo responsabilidade do backend (todas as queries já fazem) — frontend nunca confia em input do cliente para escopo do usuário.

## Risks / Trade-offs

- [Migração de schema (`professor` em `subjects`)] → Campo opcional, registros antigos ficam com null. Sem perda de dados, mas a UI exige professor no cadastro novo — assume-se que o usuário aceita preencher.
- [Mudança em `secrets.toml`] → Quebra a configuração atual: `xano_base_url` deixa de existir; usuário precisa criar `xano_auth_base_url` + `xano_subjects_base_url`. Mensagem de erro do helper indica o que falta.
- [`st.dialog` é stateful (Streamlit 1.35+)] → Bem suportado em 1.57, mas o fluxo `confirmar/cancelar` exige callbacks ou `st.session_state` para acionar `st.rerun()` após a ação. Documentado no design.
- [Operações em duplicado dependem de race] → Verificação em dois passos (`db.query` + `db.add`) tem janela teórica de race. Aceitável para v1; idealmente um índice único na tabela mas isso é uma change separada.
- [Implementação `.xs`] → Sintaxe usada já foi validada em produção em changes anteriores; mantém-se conservador.
