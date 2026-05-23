## Context

Tabela `academic_tasks` já existe ([tables/837133_academic_tasks.xs](tables/837133_academic_tasks.xs)) com campos: `id`, `created_at`, `updated_at`, `archived_at`, `title`, `description`, `due_date`, `status`, `subject_id`, `user_id`. Nenhuma function/endpoint foi criada ainda. Frontend [pages/2_📝_Tarefas.py](pages/2_📝_Tarefas.py) é mockup. Helper [lib/xano_client.py](lib/xano_client.py) suporta multi-grupo (`auth`, `subjects`); ganha mais um grupo aqui. Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- CRUD completo de `academic_tasks` no Xano com ownership e isolamento por `user_id`.
- Tela funcional com 4 abas: Listar (ativas), Nova, Calendário, Histórico.
- Sinal nativo de prazo vencido sem CSS customizado.
- Calendário visual com `streamlit-calendar`.

**Non-Goals:**
- Tema/visual (Dark Modern adiado).
- Notificações, recorrência, sub-tarefas, anexos.
- Testes automatizados; push/deploy.

## Decisions

### Backend Xano

- **Diretórios novos:** `functions/academic_tasks/` e `apis/academic_tasks/`.
- **`api_group academic_tasks`** com tag `["edutrack"]` (a URL completa será resolvida via canonical específico do grupo).
- **Funções (padrão API fina → função reutilizável, como em `subjects`):**
  - `create_task` — valida `title` não vazio; valida ownership do `subject_id` (`db.get subjects` + `precondition $subject.user_id == $auth.id`); grava `user_id = $auth.id`.
  - `list_tasks(subject_id?, status?, only_overdue?)` — `db.query academic_tasks` com `where` combinando filtros. Filtro overdue: `status != "done" && due_date < "now"`.
  - `update_task` — `db.get` + precondition de ownership + `db.edit`.
  - `delete_task` — `db.get` + precondition + `db.del`.
  - `complete_task` — atalho que `db.edit` com `status = "done"` + `updated_at = "now"`, com precondition de ownership.
- **Endpoints (todos `auth = "user"`, tag `edutrack`):**
  - `POST /academic_tasks` → `create_task`
  - `GET /academic_tasks?subject_id=&status=&only_overdue=` → `list_tasks`
  - `PATCH /academic_tasks/{id}` → `update_task`
  - `DELETE /academic_tasks/{id}` → `delete_task`
  - `POST /academic_tasks/{id}/complete` → `complete_task`
- **Status canônicos:** `pending` (default), `in_progress`, `done`. Display PT-BR só na UI.
- **Sintaxe XanoScript:** apenas operadores já validados em produção: `db.add academic_tasks`, `db.edit`, `db.get`, `db.query`, `db.del`, `precondition`, `$auth.id`, `==`, `&&`, `!=`, `<`.

### Helper Streamlit

- **Novo grupo `"academic_tasks"`** em `_SECRET_KEY_BY_GROUP`, lendo `xano_academic_tasks_base_url`.
- **Funções públicas:**
  - `tasks_list(*, subject_id=None, status=None, only_overdue=None)` — `GET`, params omitidos quando `None`.
  - `tasks_create(title, *, subject_id, description=None, due_date=None, status="pending")` — `POST`.
  - `tasks_update(task_id, *, title=None, description=None, due_date=None, status=None, subject_id=None)` — `PATCH`, payload omite `None`.
  - `tasks_delete(task_id)` — `DELETE`.
  - `tasks_complete(task_id)` — `POST .../complete`.
- **Datas:** `due_date` enviada como `YYYY-MM-DD` (formato ISO date). Helper aceita `datetime.date` e converte via `isoformat()`.
- **Subjects para selectbox:** reutilizar `subjects_list()` filtrando `archived_at == null` no client.

### Frontend `pages/2_📝_Tarefas.py`

- **4 abas:** `📋 Listar` (ativas) / `➕ Nova Tarefa` / `📅 Calendário` / `📦 Histórico`.
- **Filtros (no topo, fora das abas, em `st.form` para evitar re-fetch a cada tecla):**
  - `st.text_input` "Buscar por título" (filtro client-side simples — search by name não é suportado no GET, evita endpoint extra).
  - `st.selectbox` "Status" com opções "Todos" / "Pendente" / "Em andamento" / "Concluída".
  - `st.checkbox` "Apenas atrasadas".
- **Carregamento:** uma única chamada `tasks_list(status=..., only_overdue=...)` no início da página; filtros client-side complementam (título, agrupamento, separação ativas vs arquivadas).
- **Split ativas vs arquivadas (client-side):** carrega `subjects_list()` (todas, com `archived_at`), mapeia `subject_id → is_archived`. Tarefa entra em "Histórico" se sua disciplina está arquivada.
- **Linha de tarefa (`st.container(border=True)` + `st.columns`):**
  - Colunas: `[5, 2, 2, 2, 1, 1, 1]` → Título / Disciplina / Prazo / Status / `✓` / `✏️` / `🗑️`.
  - Se atrasada: prefixa `⚠️` no título; `st.error("Vencida em DD/MM/YYYY")` abaixo do conteúdo via subcontainer; ou usar `st.markdown(":red[...]")` (Markdown nativo do Streamlit suporta `:color[texto]` — não é HTML inseguro).
- **Aba Nova Tarefa:** `st.form(clear_on_submit=True)` com `title*`, `description`, `due_date` (`st.date_input`), `subject_id` (`st.selectbox` de ativas — label "Disciplina *"), `status` (default "Pendente"). Submit → `tasks_create`.
- **Aba Calendário:** `streamlit-calendar` com `events=[{title, start, id}]` derivado das tarefas ativas; on-click captura `eventClick` e abre `@st.dialog` de edição.
- **Aba Histórico:** itera disciplinas arquivadas, cria `st.expander` por disciplina, lista tarefas dentro com mesmos controles (ou somente leitura — decisão: manter Editar e Excluir; sem Concluir).
- **Dialogs:** `@st.dialog("Editar tarefa")` reutilizado em todas as abas; `@st.dialog("Confirmar exclusão")` para delete.
- **Flash:** `st.session_state["task_flash_success"]` igual ao padrão de disciplinas.
- **SessionExpired:** mesmo padrão das outras páginas.

### Idioma e segurança

- Documentação/UI em português; nomes técnicos/endpoints em inglês.
- `user_id` sempre via `$auth.id`; subject ownership validada antes de criar/editar.

## Risks / Trade-offs

- [Nova dependência `streamlit-calendar`] → Wrapper estável do FullCalendar (~5k downloads/dia). Adiciona ao `requirements.txt`. Sem fallback caso o componente falhe (degradação aceitável: aba mostra erro nativo).
- [Filtros server-side vs client-side] → Server faz `status` e `only_overdue`; client faz busca textual e agrupamento. Mantém endpoint simples e UI responsiva.
- [Sem search textual no backend] → Aceitável v1 — tarefas tipicamente são poucas por usuário. Se virar gargalo, evolui para `/academic_tasks/search` em v2.
- [`due_date` como `date`, não `datetime`] → Alinhado ao schema atual (`date due_date`). Hora não é capturada; "atrasada" usa comparação por dia.
- [Setup do canonical do api_group no Xano] → Precisa criar o grupo no dashboard antes do push das APIs. Documentar no commit final.
