# Change: tasks-module-v1

## Why

A tabela `academic_tasks` foi criada na change `create-academic-tasks-table`, mas o aluno ainda não consegue gerenciar tarefas — não há functions, endpoints nem tela real. A página [pages/2_📝_Tarefas.py](pages/2_📝_Tarefas.py) é um mockup estático. Esta change entrega o módulo completo, ponta a ponta, com calendário e histórico de disciplinas arquivadas.

## What Changes

Escopo restrito aos 8 requisitos pedidos + 2 visualizações extras:

1. **Cadastro** — `POST /academic_tasks` com `title` (obrigatório), `description`, `due_date`, `status`, `subject_id` (de disciplina ativa); `user_id = $auth.id`.
2. **Listagem** — `GET /academic_tasks` com filtros opcionais `subject_id`, `status`, `only_overdue`.
3. **Edição** — `PATCH /academic_tasks/{id}` com ownership via `precondition`.
4. **Exclusão** — `DELETE /academic_tasks/{id}` com ownership + confirmação nativa (`@st.dialog`).
5. **Marcar concluída** — atalho `POST /academic_tasks/{id}/complete` (ou `PATCH ... status="done"`); botão `✓` na linha.
6. **Filtro por status** — selectbox `pending` / `in_progress` / `done` (display PT-BR).
7. **Sinal de prazo vencido** — `⚠️` no título + `due_date` em `st.error` inline (`status != "done"` e `due_date < hoje`).
8. **Agrupamento** — radio na aba Listar: por Disciplina **ou** por Prazo.
9. **📅 Calendário mensal** — biblioteca `streamlit-calendar` (nova dependência); click em tarefa abre dialog de edição.
10. **📦 Histórico** — aba dedicada com tarefas de disciplinas arquivadas, agrupadas em `st.expander` por disciplina.

Valores de `status`: `pending`, `in_progress`, `done` (canônico `done` alinhado ao `calculate_progress.py` e ao filtro overdue de `subjects`).

Fora de escopo: visual/tema (Dark Modern adiado), notificações/push, recorrência de tarefas, anexos, sub-tarefas, testes automatizados, push/deploy.

## Capabilities

### New Capabilities
- `tasks-module`: Gestão de tarefas acadêmicas (academic_tasks) com CRUD, marcar concluída, filtros, agrupamento, sinal de prazo vencido, calendário mensal e histórico de disciplinas arquivadas.

### Modified Capabilities
<!-- Nenhuma capability existente tem requisitos alterados. -->

## Impact

- **Backend Xano (criação do zero):**
  - Novo diretório `functions/academic_tasks/` com `create_task`, `list_tasks`, `update_task`, `delete_task`, `complete_task`
  - Novo `apis/academic_tasks/` com endpoints CRUD + atalho complete + `api_group.xs`
  - Reaproveita tabela `academic_tasks` já existente
- **Helper Streamlit:** [lib/xano_client.py](lib/xano_client.py) ganha grupo `academic_tasks` + funções `tasks_*`
- **Frontend:** [pages/2_📝_Tarefas.py](pages/2_📝_Tarefas.py) reescrita totalmente
- **Secrets:** `.streamlit/secrets.toml.example` ganha `xano_academic_tasks_base_url`
- **Dependência:** `streamlit-calendar` em `requirements.txt`
- **Sem push/deploy** (AGENTS.md Regra Nº2).
