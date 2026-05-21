## Context

A v1 (`disciplines-frontend-integration-v1`) está arquivada com spec permanente em [openspec/specs/disciplines-frontend/spec.md](openspec/specs/disciplines-frontend/spec.md). Helper multi-grupo, auth e CRUD de subjects funcionando ponta-a-ponta. Os endpoints `POST /subjects/{id}/archive` e `POST /subjects/{id}/unarchive` já existem no backend (auditados na change `verify-subjects-crud-auth`), mas não há UI consumindo. Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Adicionar `workload_hours` e `semester` em `subjects` e propagar pelos endpoints.
- UI completa de arquivamento (aba dedicada, ações por linha).
- Reformatar a listagem com ações por linha em vez de expander.

**Non-Goals:**
- Visual/tema (Dark Modern adiado).
- Paginação/ordenação avançada, filtro por semestre na barra de busca (pode entrar em v3 se necessário).
- Push/deploy.

## Decisions

### Schema

- `text workload_hours?` — não, melhor **`int workload_hours?`** (inteiro de horas, opcional). Permite somar futuramente.
- `int semester?` — inteiro do período do curso (1, 2, 3…). Opcional para preservar registros antigos.
- Tipos opcionais (`?`) seguem o padrão já adotado em v1 para `professor` e `description`.

### Backend

- **`create_subject`** e **`update_subject`** ganham `int workload_hours?` e `int semester?` nos inputs e persistem nos `db.add.data`/`db.edit.data`.
- **API `POST` / `PATCH`** declaram os novos inputs como opcionais e repassam via `function.run`.
- **Duplicado** continua sendo `(user_id, name, professor)` — `workload_hours` e `semester` NÃO entram no critério de duplicado (mesma matéria em semestres diferentes não é "duplicada").
- **Archive/unarchive functions e APIs** não mudam.
- **Sintaxe XanoScript:** apenas operadores já validados em produção (`db.add subjects {...}`, `db.edit`, `db.get`, `db.query`, `precondition`, `$auth.id`, `==`, `&&`).

### Helper Streamlit

- `subjects_create(name, professor, description="", workload_hours=None, semester=None)` — campos opcionais. Payload omite os `None`.
- `subjects_update(id, *, name=None, professor=None, description=None, workload_hours=None, semester=None)` — mesma lógica.
- `subjects_archive(subject_id)` → `POST /subjects/{id}/archive`.
- `subjects_unarchive(subject_id)` → `POST /subjects/{id}/unarchive`.
- Split ativas/arquivadas é **client-side** pelo campo `archived_at` da resposta. Evita backend novo.

### Frontend (`pages/1_📚_Disciplinas.py`)

- Barra de busca + checkbox "atrasadas" continua no topo, alimentando `subjects_search`.
- **3 abas:** `📋 Listar ativas`, `➕ Nova Disciplina`, `📦 Arquivadas`.
- **Listagem por linha** (sem `st.dataframe`):
  - `st.container(border=True)` por disciplina.
  - Dentro: `st.columns([3, 2, 1, 1, 1, 1, 1])` com colunas Nome / Professor / Carga / Semestre / Editar / Arquivar(ou Desarquivar) / Excluir.
- **Form Nova:** `name *`, `professor *`, `workload_hours` (`st.number_input` min_value=0 step=1), `semester` (`st.number_input` min_value=1 step=1), `description` (text_area). `clear_on_submit=True`.
- **Edit dialog** (`@st.dialog`): mesma estrutura do form com valores pré-preenchidos.
- **Confirm dialog** para Excluir mantido.
- **Flash de sucesso** via `st.session_state["disc_flash_success"]` mantido para cadastro/edição/arquivar/desarquivar/excluir.
- Tratamento de `SessionExpired` igual à v1.

### Idioma e segurança

- Documentação/UI em português; nomes técnicos/endpoints em inglês.
- `user_id` continua filtrado no backend (defense in depth).

## Risks / Trade-offs

- [Mais uma migração de schema] → Adição de campos opcionais, sem perda de dados. Igual à migração do `professor` — Xano emite aviso, mas é seguro.
- [Listagem por linha com `st.columns`] → Mais flexível que `st.dataframe` para ações, mas com muitas disciplinas pode ficar verticalmente longo. Aceitável para v2.
- [Split client-side de archived] → Funciona porque a resposta inclui `archived_at`. Se o backend mudar para excluir esse campo, o split quebra. Improvável.
- [Filtro de overdue em arquivadas] → A query atual de `search_subjects` filtra por subjects com tarefas overdue. Disciplinas arquivadas podem ter tarefas overdue ainda — aceitamos por simplicidade; refinamento futuro se necessário.
