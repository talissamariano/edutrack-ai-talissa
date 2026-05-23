## 1. Funções Xano

- [x] 1.1 Criar `functions/academic_tasks/create_task.xs` (valida `title` não vazio, valida ownership do `subject_id` via `db.get subjects` + precondition, grava `user_id = $auth.id`)
- [x] 1.2 Criar `functions/academic_tasks/list_tasks.xs` (`db.query academic_tasks` com `where = user_id == $auth.id`, combinando filtros opcionais `subject_id`, `status` e overdue)
- [x] 1.3 Criar `functions/academic_tasks/update_task.xs` (`db.get` + precondition de ownership + `db.edit`)
- [x] 1.4 Criar `functions/academic_tasks/delete_task.xs` (`db.get` + precondition + `db.del`)
- [x] 1.5 Criar `functions/academic_tasks/complete_task.xs` (atalho `db.edit` com `status = "done"`, com precondition de ownership)

## 2. APIs Xano

- [x] 2.1 Criar `apis/academic_tasks/api_group.xs` com `api_group academic_tasks` e tag `["edutrack"]`
- [x] 2.2 Criar `apis/academic_tasks/.../academic_tasks_POST.xs` → chama `create_task`
- [x] 2.3 Criar `apis/academic_tasks/.../academic_tasks_GET.xs` (inputs `subject_id?`, `status?`, `only_overdue?`) → chama `list_tasks`
- [x] 2.4 Criar `apis/academic_tasks/.../academic_tasks_id_PATCH.xs` → chama `update_task`
- [x] 2.5 Criar `apis/academic_tasks/.../academic_tasks_id_DELETE.xs` → chama `delete_task`
- [x] 2.6 Criar `apis/academic_tasks/.../academic_tasks_id_complete_POST.xs` → chama `complete_task`

## 3. Helper Streamlit

- [x] 3.1 Adicionar grupo `"academic_tasks"` em `_SECRET_KEY_BY_GROUP` em `lib/xano_client.py`, lendo `xano_academic_tasks_base_url`
- [x] 3.2 Adicionar `tasks_list`, `tasks_create`, `tasks_update`, `tasks_delete`, `tasks_complete` em `lib/xano_client.py`
- [x] 3.3 Atualizar `.streamlit/secrets.toml.example` com `xano_academic_tasks_base_url`
- [x] 3.4 Adicionar `streamlit-calendar` em `requirements.txt`

## 4. Tela de Tarefas

- [x] 4.1 Reescrever `pages/2_📝_Tarefas.py` com 4 abas: "📋 Listar", "➕ Nova Tarefa", "📅 Calendário", "📦 Histórico"
- [x] 4.2 Barra de filtros (busca por título, status, apenas atrasadas) acima das abas
- [x] 4.3 Carregar uma vez `tasks_list(...)` e `subjects_list()` (com archived) para split ativas vs arquivadas no client
- [x] 4.4 Aba "Listar": radio "Agrupar por Disciplina"/"Agrupar por Prazo"; linhas com `st.container(border=True)` + `st.columns`; botões `✓` / `✏️` / `🗑️` icon-only com `help`
- [x] 4.5 Sinal de atrasada: `⚠️` antes do título e prazo em destaque (st.markdown com `:red[...]` ou `st.error` inline; sem `unsafe_allow_html=True`)
- [x] 4.6 Aba "Nova Tarefa": `st.form(clear_on_submit=True)` com `title*`, `description`, `due_date` (`st.date_input`), `subject_id` (`st.selectbox` só de ativas), `status` (default Pendente); submit → `tasks_create` + flash + rerun
- [x] 4.7 Aba "Calendário": integrar `streamlit-calendar` com eventos derivados das tarefas ativas; `eventClick` abre dialog de edição
- [x] 4.8 Aba "Histórico": iterar disciplinas arquivadas e criar `st.expander` por disciplina com tarefas dentro (com ações Editar/Excluir, sem Concluir)
- [x] 4.9 `@st.dialog` "Editar tarefa" reutilizado em todas as abas; `@st.dialog` "Confirmar exclusão" para delete
- [x] 4.10 Botão `✓` chama `tasks_complete` direto + flash + rerun
- [x] 4.11 Tratar `xano.SessionExpired` em todas as chamadas (`_session_expired_notice` + `st.rerun`)
- [x] 4.12 Verificar ausência de `unsafe_allow_html=True` para estilo
