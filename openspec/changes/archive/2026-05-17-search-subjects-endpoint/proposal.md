## Why

O aluno precisa localizar disciplinas rapidamente — seja pelo nome, seja para focar nas que têm tarefas atrasadas. Hoje o `GET /subjects` apenas lista; falta um endpoint de busca com esses filtros.

## What Changes

- Criar um endpoint de busca de `subjects` para o usuário autenticado.
- Suportar dois modos de filtro (OU): por `name` (correspondência textual) **ou** por disciplinas que possuem `academic_tasks` atrasadas.
- "Tarefa atrasada" usa o mesmo critério da lógica Python existente (`calculate_progress.py`): tarefa com `status != "done"` e `due_date < agora`.
- Toda a busca restrita ao `user_id` do usuário autenticado (segurança AGENTS.md).

Fora de escopo (não solicitado): paginação, ordenação avançada, CRUD adicional, alterações em `academic_tasks`, testes automatizados, push/deploy.

## Capabilities

### New Capabilities
- `subjects-search`: Busca de disciplinas do usuário autenticado por nome ou por presença de tarefas atrasadas.

### Modified Capabilities
<!-- Nenhuma capability permanente existente tem requisitos alterados. -->

## Impact

- **Nova API:** um endpoint de busca em `apis/subjects/` (ex.: `GET /subjects/search`).
- **Nova função:** lógica de busca em `functions/subjects/` (padrão das funções existentes).
- **Depende de:** tabelas `subjects` e `academic_tasks` (já existentes).
- **Reaproveita conceito de:** `scripts/calculate_progress.py` (critério de "atrasada"), reimplementado em XanoScript.
- **Sem push/deploy:** entrega limitada à geração dos arquivos (AGENTS.md Regra Nº2).
