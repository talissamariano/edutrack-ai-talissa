# Change: dashboard-and-progress-v1

## Why

A Home atual ([home.py](home.py)) é estática, com métricas hardcoded como "0". O professor pediu, na revisão do projeto, uma tela inicial com visão geral pós-login (totais, próximas tarefas, % de progresso) e indicadores nas Disciplinas. Esta change entrega a 1ª onda dessas melhorias **sem novos endpoints nem migração de schema** — só agregando, no Streamlit, dados que já temos.

## What Changes

Escopo restrito aos itens da 1ª onda das melhorias do professor:

### A — Dashboard na Home
A Home passa a exibir, após o login:
- **Total de disciplinas ativas** (não arquivadas)
- **Total de tarefas pendentes** (`status != "done"`)
- **Total de tarefas atrasadas** (`status != "done"` **e** `due_date < hoje`)
- **Próximas 5 tarefas** (pendentes, ordenadas por `due_date` asc)
- **% de progresso geral** (concluídas/total) usando o `scripts/calculate_progress.py` que já existe

### B — Progresso e sinais nas Disciplinas
Cada linha de disciplina ativa passa a mostrar:
- **% de progresso** (texto + `st.progress`)
- **Sinais de tarefas** — `⚠️ N atrasada(s)` e/ou `📅 N próxima(s)` (próximos 7 dias). Disciplinas sem nada não exibem o sinal.

### C — Tela de boas-vindas
Se o usuário não tem disciplinas, a Home exibe **mensagem amigável + CTA "Cadastre sua primeira disciplina"** em vez de um dashboard com zeros.

Fora de escopo: tema visual (Dark Modern/Poppins — Módulo F), relatórios/exportação (Módulo E), prioridade nas tarefas (Módulo D), testes automatizados, push/deploy.

## Capabilities

### New Capabilities
- `home-dashboard`: Tela inicial com métricas agregadas (totais, próximas tarefas, progresso geral) e estado de boas-vindas para usuários sem dados.

### Modified Capabilities
- `disciplines-frontend`: a listagem ganha **progresso** e **sinais de tarefas** por disciplina.

## Impact

- **Frontend (somente):**
  - [home.py](home.py) reescrita com dashboard + welcome
  - [pages/1_📚_Disciplinas.py](pages/1_📚_Disciplinas.py) ganha colunas "Progresso" e "Sinais" na linha
  - Reutiliza [scripts/calculate_progress.py](scripts/calculate_progress.py) (sem alterar)
- **Backend Xano:** zero — usa endpoints existentes (`GET /subjects`, `GET /academic_tasks`).
- **Schema:** zero migração.
- **Sem push/deploy** (AGENTS.md Regra Nº2).
