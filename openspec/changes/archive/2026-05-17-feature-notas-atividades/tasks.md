## 1. Tabela activity_grades

- [ ] 1.1 Criar a tabela `activity_grades` em `tables/` com os campos `id`, `created_at`, `updated_at`, `archived_at`, `student_id`, `activity_id`, `grade` e `user_id` (FK → `user`), seguindo o padrão da tabela `subjects` (delegar ao Xano Table Designer)
- [ ] 1.2 Adicionar índices: `primary` em `id` e `btree` em `user_id`

## 2. API POST /activity_grades

- [ ] 2.1 Criar o endpoint `POST /activity_grades` em `apis/` com autenticação obrigatória (delegar ao Xano API Query Writer)
- [ ] 2.2 Validar os inputs `student_id`, `activity_id` (obrigatórios) e `grade` (obrigatório, dentro do intervalo válido)
- [ ] 2.3 Gravar o registro vinculando `user_id` ao professor autenticado (a partir do token, nunca do input)
- [ ] 2.4 Retornar a nota criada na resposta
