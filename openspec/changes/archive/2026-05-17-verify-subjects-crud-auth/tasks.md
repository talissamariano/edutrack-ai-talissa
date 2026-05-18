## 1. Auditoria de autenticação e ownership

- [x] 1.1 Reler os 6 arquivos de API em `apis/subjects/` e suas funções em `functions/subjects/`
- [x] 1.2 Verificar `auth = "user"` em `POST /subjects` e em sua função (grava `user_id = $auth.id`)
- [x] 1.3 Verificar `auth = "user"` em `GET /subjects` e filtro `where user_id == $auth.id` na função
- [x] 1.4 Verificar `auth = "user"` no update e `precondition` de ownership (`user_id == $auth.id`) na função
- [x] 1.5 Verificar `auth = "user"` em `DELETE /subjects/{id}` e `precondition` de ownership na função
- [x] 1.6 Verificar `auth = "user"` em `archive` e `unarchive` e `precondition` de ownership nas funções
- [x] 1.7 Registrar o resultado da auditoria em um checklist por endpoint (conforme / não conforme)

## 2. Adaptação dos endpoints não conformes

- [x] 2.1 Para cada endpoint sem `auth = "user"`, adicioná-lo (delegar ao Xano API Query Writer) — N/A: todos já possuem `auth = "user"`
- [x] 2.2 Para cada operação sem isolamento por `user_id`, adicionar o filtro/precondition correspondente — N/A: todos já isolam por `user_id`
- [x] 2.3 Realinhar o endpoint de atualização de `PUT` para `PATCH /subjects/{id}` (ajustar `verb` e nome do arquivo), mantendo a função `update_subject`
