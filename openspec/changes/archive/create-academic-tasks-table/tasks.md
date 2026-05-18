## 1. Tabela academic_tasks

- [x] 1.1 Criar a tabela `academic_tasks` em `tables/` seguindo o padrão da tabela `subjects` (delegar ao Xano Table Designer)
- [x] 1.2 Definir os campos: `id` (int), `created_at`/`updated_at`/`archived_at` (timestamp), `title` (text, filters=trim), `description` (text), `due_date` (date), `status` (text)
- [x] 1.3 Definir a FK `subject_id` (int) referenciando a tabela `subjects`
- [x] 1.4 Definir a FK `user_id` (int) referenciando a tabela `user`
- [x] 1.5 Adicionar índices: `primary` em `id`, `btree` em `user_id`, `btree` em `subject_id` e `btree` em `created_at desc`
- [x] 1.6 Adicionar a tag `["edutrack"]`
