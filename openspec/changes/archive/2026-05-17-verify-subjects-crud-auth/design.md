## Context

O Xano gera CRUD automático e o projeto já possui, em `apis/subjects/` e `functions/subjects/`, os endpoints: `POST /subjects`, `GET /subjects`, `PUT /subjects/{id}`, `DELETE /subjects/{id}`, `POST /subjects/{id}/archive`, `POST /subjects/{id}/unarchive`. Esta change é uma **auditoria + adaptação** desses endpoints existentes, não uma recriação.

## Goals / Non-Goals

**Goals:**
- Confirmar `auth = "user"` em todos os 6 endpoints.
- Confirmar isolamento por `user_id` (filtro na query ou `precondition` de ownership) em cada operação.
- Alinhar o verbo de atualização para `PATCH` conforme AGENTS.md.

**Non-Goals:**
- Recriar o CRUD ou as funções do zero.
- Novas tabelas/funcionalidades, testes automatizados.
- Push/sync/deploy.

## Decisions

- **Estado atual observado (inspeção prévia):**
  - `POST /subjects` → `auth=user`; função grava `user_id = $auth.id`. ✔️
  - `GET /subjects` → `auth=user`; função filtra `where user_id == $auth.id`. ✔️
  - `PUT /subjects/{id}` → `auth=user`; função tem `precondition ($subject.user_id == $auth.id)`. ✔️ auth/ownership, ⚠️ verbo `PUT` diverge do padrão `PATCH`.
  - `DELETE /subjects/{id}` → `auth=user`; ownership via `precondition`. ✔️
  - `POST /subjects/{id}/archive` → `auth=user`; ownership via `precondition`. ✔️
  - `POST /subjects/{id}/unarchive` → `auth=user`; ownership via `precondition`. ✔️
- **Abordagem da auditoria:** ler cada arquivo `.xs` e checar dois critérios objetivos por endpoint — (1) `auth = "user"`; (2) presença de filtro/precondition por `user_id`. Registrar o resultado em checklist.
- **Adaptação principal:** realinhar o endpoint de atualização de `PUT` para `PATCH` (renomear o arquivo de API e ajustar `verb=PATCH`), mantendo a função `update_subject` inalterada.
  - *Alternativa considerada:* manter `PUT` — descartada porque o usuário pediu explicitamente `PATCH` e o AGENTS.md define `PATCH` como padrão de atualização.
- **Implementação XanoScript:** delegar ajustes ao agente especializado (Xano API Query Writer); `openspec/AGENTS.md` e `docs/*_guideline.md` não existem → usar a seção `# XanoScript Instructions` do AGENTS.md como fallback.

## Risks / Trade-offs

- [Renomear `PUT`→`PATCH` pode quebrar clientes que já chamam `PUT`] → Mitigação: o frontend Streamlit ainda está em desenvolvimento; alinhar agora evita dívida. Documentar a mudança de contrato.
- [Auditoria depende de leitura estática dos `.xs`] → Suficiente para os critérios auth/ownership; validação de runtime fica a cargo do desenvolvedor (sem deploy nesta change).
- [Endpoints podem mudar antes da implementação] → A task de auditoria deve reler os arquivos no momento da aplicação, não confiar só neste snapshot.
