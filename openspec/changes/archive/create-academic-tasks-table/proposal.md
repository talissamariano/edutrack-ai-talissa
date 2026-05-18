## Why

O EduTrack AI permite gerenciar disciplinas (`subjects`), mas o aluno ainda não tem onde registrar suas obrigações acadêmicas (lições, provas, trabalhos) e acompanhar prazos e status. É necessário um modelo de dados para essas obrigações vinculadas a cada disciplina.

## What Changes

- Criar a tabela `academic_tasks` para armazenar obrigações acadêmicas do aluno.
- Campos: `title` (text), `description` (text), `due_date` (date), `status` (text), `subject_id` (FK → `subjects`).
- Adicionar `user_id` (FK → `user`) para vincular cada obrigação ao aluno autenticado (segurança obrigatória do AGENTS.md).
- Campos de auditoria e índices seguindo o padrão da tabela `subjects`.

Fora de escopo (não solicitado): APIs/CRUD, telas Streamlit, automações.

## Capabilities

### New Capabilities
- `academic-tasks`: Estrutura de banco de dados para o aluno registrar e gerenciar obrigações acadêmicas vinculadas a uma disciplina.

### Modified Capabilities
<!-- Nenhuma capability existente tem requisitos alterados. -->

## Impact

- **Banco de dados:** nova tabela `academic_tasks` em `tables/`.
- **Relacionamentos:** `subject_id` → `subjects`; `user_id` → `user`.
- **Sem push/deploy:** entrega limitada à geração dos arquivos (AGENTS.md Regra Nº2).
