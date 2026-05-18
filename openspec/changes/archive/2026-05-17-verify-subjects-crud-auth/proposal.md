## Why

O Xano gera CRUD automaticamente e já existem endpoints de `subjects` (POST, GET, update, DELETE, archive, unarchive). É necessário garantir, por auditoria, que **todos** esses endpoints exigem autenticação e que cada usuário só acessa os próprios dados — e adaptar os que não estiverem em conformidade, em vez de recriar o CRUD.

## What Changes

- Auditar todos os endpoints existentes de `subjects` quanto a: `auth = "user"` e isolamento por `user_id` do usuário autenticado.
- Endpoints no escopo da verificação: `POST /subjects`, `GET /subjects`, atualização (`PUT/PATCH /subjects/{id}`), `DELETE /subjects/{id}`, `POST /subjects/{id}/archive`, `POST /subjects/{id}/unarchive`.
- Alinhar o verbo de atualização para **PATCH** (`PATCH /subjects/{id}`), conforme padrão RESTful do AGENTS.md (hoje implementado como `PUT`).
- Adaptar qualquer endpoint que não imponha autenticação ou não filtre/valide por `user_id`.

Fora de escopo (não solicitado): recriar o CRUD do zero, novas tabelas, novas funcionalidades, testes automatizados, push/deploy.

## Capabilities

### New Capabilities
- `subjects-access-control`: Regras que garantem que toda operação sobre `subjects` exige usuário autenticado e restringe o acesso aos registros do próprio usuário.

### Modified Capabilities
<!-- Não há specs permanentes de subjects em openspec/specs/; nenhuma capability existente tem requisitos alterados. -->

## Impact

- **APIs auditadas:** `apis/subjects/*` (6 endpoints).
- **Funções auditadas:** `functions/subjects/*` (create, list, update, delete, archive, unarchive).
- **Possível adaptação:** renomear/realinhar o endpoint de atualização de `PUT` para `PATCH`.
- **Sem push/deploy:** entrega limitada à verificação e geração/ajuste dos arquivos (AGENTS.md Regra Nº2).
