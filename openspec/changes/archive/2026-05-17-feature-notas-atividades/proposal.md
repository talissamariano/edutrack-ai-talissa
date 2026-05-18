## Why

Atualmente o EduTrack AI não possui forma de o professor registrar o desempenho dos alunos. Para acompanhar o progresso acadêmico, o professor precisa lançar notas para alunos em atividades específicas.

## What Changes

- Criar a tabela `activity_grades` para armazenar a nota de um aluno em uma atividade específica.
- Criar uma API **POST `/activity_grades`** para o professor autenticado lançar uma nota.
- Toda operação é vinculada ao professor autenticado via `user_id` (filtro obrigatório de segurança).

Fora de escopo (não solicitado): listagem/consulta (GET), edição (PATCH) e exclusão (DELETE) de notas.

## Capabilities

### New Capabilities
- `activity-grades`: Permite que o professor autenticado lance a nota de um aluno em uma atividade específica, persistindo o registro associado ao professor.

### Modified Capabilities
<!-- Nenhuma capability existente tem requisitos alterados. -->

## Impact

- **Banco de dados:** nova tabela `activity_grades` em `tables/`.
- **APIs:** novo endpoint `POST /activity_grades` em `apis/`.
- **Premissa:** não existe tabela de atividades nem de alunos no projeto atual; a nota referenciará `activity_id` e `student_id` como inteiros. A criação dessas tabelas está fora do escopo desta change.
- **Sem push/deploy:** entrega limitada à geração dos arquivos (AGENTS.md Regra Nº2).
