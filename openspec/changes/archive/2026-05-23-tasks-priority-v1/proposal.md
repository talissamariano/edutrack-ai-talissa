# Change: tasks-priority-v1

## Why

O professor pediu, entre as melhorias, "campo de prioridade nas tarefas (Baixa, Média, Alta)". Hoje todas as tarefas têm o mesmo peso visual e a única ordem é por prazo. Adicionar prioridade ajuda o aluno a se organizar melhor — distinguir uma prova importante de uma leitura opcional, por exemplo.

## What Changes

Escopo restrito ao Módulo D das melhorias:

1. **Schema:** novo campo `priority` (text, opcional) em `academic_tasks`. Valores canônicos: `"low"`, `"medium"`, `"high"`.
2. **Backend:** `create_task` e `update_task` aceitam e persistem `priority`; APIs `POST`/`PATCH`/`GET` declaram/repassam; `GET` ganha `priority` como filtro opcional.
3. **Helper:** `tasks_create`, `tasks_update` e `tasks_list` aceitam `priority`.
4. **Frontend `pages/2_📝_Tarefas.py`:**
   - Form Nova: selectbox "Prioridade" (Baixa / Média / Alta), default Média.
   - Dialog Editar: mesmo selectbox pré-preenchido.
   - Barra de filtros: novo selectbox "Prioridade" (Todas / Baixa / Média / Alta).
   - Linha de tarefa: badge com emoji (🟢 Baixa / 🟡 Média / 🔴 Alta / ⚪ Sem prioridade).

Fora de escopo: ordenação por prioridade, relatórios (Módulo E), tema visual (Módulo F), testes automatizados, push/deploy.

## Capabilities

### New Capabilities
<!-- Nenhuma capability nova; expande a tasks-module existente. -->

### Modified Capabilities
- `tasks-module`: tarefas ganham o atributo `priority` (criação, edição, filtro e exibição).

## Impact

- **Schema Xano:** [tables/837133_academic_tasks.xs](tables/837133_academic_tasks.xs) ganha `text priority?`
- **Backend Xano:**
  - [functions/academic_tasks/310161_create_task.xs](functions/academic_tasks/310161_create_task.xs) — aceita e grava `priority`
  - [functions/academic_tasks/310163_update_task.xs](functions/academic_tasks/310163_update_task.xs) — aceita e grava `priority`
  - [functions/academic_tasks/310162_list_tasks.xs](functions/academic_tasks/310162_list_tasks.xs) — aceita filtro `priority` opcional
  - [apis/academic_tasks/3894336_academic_tasks_POST.xs](apis/academic_tasks/3894336_academic_tasks_POST.xs) — input + forward
  - [apis/academic_tasks/3894337_academic_tasks_GET.xs](apis/academic_tasks/3894337_academic_tasks_GET.xs) — input + forward
  - [apis/academic_tasks/3894338_academic_tasks_id_PATCH.xs](apis/academic_tasks/3894338_academic_tasks_id_PATCH.xs) — input + forward
- **Helper:** [lib/xano_client.py](lib/xano_client.py) — `tasks_create`, `tasks_update`, `tasks_list` aceitam `priority`
- **Frontend:** [pages/2_📝_Tarefas.py](pages/2_📝_Tarefas.py) — form, dialog, filtro e linha
- **Sem push/deploy** (AGENTS.md Regra Nº2). Push manual no Xano será necessário (6 `.xs`).
