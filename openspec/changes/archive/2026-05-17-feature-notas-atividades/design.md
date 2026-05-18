## Context

O EduTrack AI possui backend em XanoScript com Spec-Driven Development. Hoje existem as tabelas `user` (autenticação nativa do Xano) e `subjects`. Não existe tabela de atividades nem de alunos. O professor precisa lançar notas para alunos em atividades específicas. A entrega se limita à geração de arquivos (sem push/deploy — AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Tabela `activity_grades` para persistir a nota de um aluno em uma atividade.
- Endpoint `POST /activity_grades` autenticado para o professor lançar a nota.
- Toda escrita vinculada ao `user_id` do professor autenticado.

**Non-Goals:**
- APIs GET/listagem/consulta de notas.
- APIs PATCH/DELETE (edição/exclusão).
- Criação de tabelas `activities` ou `students`.
- Push/sync/deploy para o Xano.

## Decisions

- **Modelagem da tabela `activity_grades`** (`snake_case`, inglês): `id` (int, PK), `created_at`/`updated_at`/`archived_at` (timestamp), `student_id` (int), `activity_id` (int), `grade` (decimal), `user_id` (int, FK → `user`). Segue o padrão da tabela `subjects` existente.
  - *Alternativa considerada:* FKs reais para `activities`/`students` — descartada porque essas tabelas não existem e criá-las está fora do escopo. Usamos inteiros simples com a premissa registrada na proposal.
- **Endpoint `POST /activity_grades`** com `auth` habilitado; obtém o professor pelo token e grava `user_id` a partir do usuário autenticado (nunca do input do cliente) — segurança AGENTS.md.
- **Validação de entrada:** `student_id`, `activity_id` obrigatórios; `grade` obrigatório e dentro de um intervalo válido (ex.: 0 a 10).
- **Idioma:** documentação em português; nomes de tabela/campos/endpoint em inglês `snake_case`.

## Risks / Trade-offs

- [`student_id`/`activity_id` sem integridade referencial real] → Aceito conscientemente; documentado como premissa. Tabelas reais podem ser introduzidas em change futura, adicionando FKs.
- [Possível nota duplicada para o mesmo aluno/atividade] → Fora do escopo atual (não foi pedido); pode ser tratado futuramente com índice único.
- [Implementação .xs deve seguir guidelines do XanoScript] → `openspec/AGENTS.md` e `docs/*_guideline.md` não existem; a implementação deverá usar a seção `# XanoScript Instructions` do `AGENTS.md` como fallback e delegar aos agentes especializados (Table Designer / API Query Writer).
