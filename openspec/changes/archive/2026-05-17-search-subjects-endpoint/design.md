## Context

O backend é XanoScript. Existem as tabelas `subjects` e `academic_tasks` (com `subject_id`, `user_id`, `due_date`, `status`). O endpoint de busca segue o padrão já usado em `subjects` (API fina → função reutilizável). O script `scripts/calculate_progress.py` define o critério de "concluída" como `status == "done"`; reaproveitamos o critério inverso para "atrasada". Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Um endpoint de busca autenticado, isolado por `user_id`.
- Filtro por `name` OU por presença de tarefas atrasadas.

**Non-Goals:**
- Paginação/ordenação avançada, CRUD adicional, alterações em `academic_tasks`.
- Execução real de código Python pelo Xano.
- Push/sync/deploy.

## Decisions

- **Endpoint:** `GET /subjects/search`, `auth = "user"`, em `apis/subjects/`, delegando a uma nova função `subjects/search_subjects` em `functions/subjects/` (mesmo padrão das demais).
- **Inputs:** `name?` (text, opcional) e `only_overdue?` (bool, opcional). Ambos opcionais; combinação por OU quando os dois vierem.
- **Filtro por nome:** correspondência textual no campo `name` (ex.: operador de contains/like do XanoScript), sempre com `user_id == $auth.id`.
- **Filtro por atrasadas:** disciplinas que têm ao menos uma `academic_task` com `user_id == $auth.id`, `status != "done"` e `due_date < "now"`.
- **"Integração da lógica Python":** o backend Xano não roda Python. Decisão: **reimplementar em XanoScript o mesmo critério** do `calculate_progress.py` (estado final = `done`), garantindo consistência conceitual.
  - *Alternativa considerada:* chamar o script `.py` externamente — descartada por inviabilidade arquitetural (Xano não executa Python arbitrário) e por estar fora do escopo pedido.
- **Implementação XanoScript:** delegar aos agentes especializados (Xano API Query Writer / Function Writer); `openspec/AGENTS.md` e `docs/*_guideline.md` não existem → usar a seção `# XanoScript Instructions` do AGENTS.md como fallback e seguir o padrão das funções `subjects/*`.

## Risks / Trade-offs

- [Interpretação de "lógica Python"] → Documentada como reimplementação do mesmo critério em XanoScript; se a intenção for outra, exige revisão antes da implementação (`/opsx:apply`).
- [Sintaxe de busca textual / subquery de atrasadas em XanoScript] → Confirmar operadores corretos no momento da implementação consultando `# XanoScript Instructions`; não assumir sintaxe.
- [Definição de "atrasada" acoplada ao critério do script] → Se o conjunto de status finais mudar, ajustar script e endpoint juntos.
