## Context

O EduTrack AI possui backend XanoScript com a tabela `subjects` (padrão de referência) e a tabela nativa `user`. O aluno precisa de um local para registrar obrigações acadêmicas vinculadas a disciplinas. Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Tabela `academic_tasks` com os campos solicitados + vínculo ao aluno.
- Consistência com o padrão da tabela `subjects` existente.

**Non-Goals:**
- APIs/CRUD, validações de aplicação, telas Streamlit.
- Criação/alteração de outras tabelas.
- Push/sync/deploy para o Xano.

## Decisions

- **Esquema da tabela `academic_tasks`** (`snake_case`, inglês):
  - `id` (int, PK)
  - `created_at`, `updated_at`, `archived_at` (timestamp) — auditoria igual a `subjects`
  - `title` (text, `filters=trim`)
  - `description` (text)
  - `due_date` (date)
  - `status` (text) — armazenado como texto conforme solicitado
  - `subject_id` (int, FK → `subjects`)
  - `user_id` (int, FK → `user`)
- **Índices:** `primary` em `id`; `btree` em `user_id` e `subject_id` (filtros mais comuns: por aluno e por disciplina); `btree` em `created_at desc` seguindo `subjects`.
- **Tag:** `["edutrack"]`, igual às demais tabelas.
- **`user_id` obrigatório:** AGENTS.md exige filtro por `user_id` do usuário autenticado; o vínculo é definido no design já no nível da tabela.
  - *Alternativa considerada:* não incluir `user_id` (apenas o solicitado) — descartada porque viola a regra de segurança do AGENTS.md e impediria isolar obrigações por aluno.

## Risks / Trade-offs

- [`status` como texto livre pode gerar valores inconsistentes] → Aceito; enum/validação não foi solicitado e pode ser tratado em change futura (ex.: `pending`, `done`).
- [Implementação .xs deve seguir guidelines do XanoScript] → `openspec/AGENTS.md` e `docs/*_guideline.md` não existem; usar a seção `# XanoScript Instructions` do `AGENTS.md` como fallback e delegar ao **Xano Table Designer**.
- [Ordem de criação de FKs] → `subjects` e `user` já existem, então `subject_id`/`user_id` podem ser definidos diretamente.
