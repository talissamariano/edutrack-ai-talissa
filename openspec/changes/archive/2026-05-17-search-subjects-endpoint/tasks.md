## 1. Função de busca

- [x] 1.1 Criar a função `subjects/search_subjects` em `functions/subjects/` seguindo o padrão das funções existentes (delegar ao Xano Function Writer)
- [x] 1.2 Definir inputs `name?` (text) e `only_overdue?` (bool)
- [x] 1.3 Implementar filtro por nome sobre `subjects` sempre com `user_id == $auth.id`
- [x] 1.4 Implementar filtro de disciplinas com `academic_tasks` atrasadas (`status != "done"` e `due_date < "now"`), restrito a `user_id == $auth.id`
- [x] 1.5 Combinar os dois filtros por OU quando ambos forem informados

## 2. Endpoint de busca

- [x] 2.1 Criar a API `GET /subjects/search` em `apis/subjects/` com `auth = "user"` (delegar ao Xano API Query Writer)
- [x] 2.2 Encaminhar os inputs para `subjects/search_subjects` via `function.run` e retornar o resultado
