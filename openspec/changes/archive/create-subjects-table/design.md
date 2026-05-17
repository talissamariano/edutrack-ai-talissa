## Context

A aplicação atualmente não possui uma maneira de os usuários gerenciarem suas disciplinas acadêmicas. A proposta é adicionar uma nova tabela `subjects` para armazenar essas informações, com um relacionamento com a tabela `users`.

## Goals / Non-Goals

**Goals:**
- Definir o esquema da tabela `subjects`.
- Especificar o relacionamento entre `subjects` e `users`.

**Non-Goals:**
- Detalhar a implementação da API ou do frontend.
- Implementar funcionalidades de automação complexas nesta fase inicial.

## Decisions

- **Esquema da Tabela `subjects`**:
  - `id`: Chave primária, tipo `INTEGER`.
  - `name`: Nome da disciplina, tipo `TEXT` ou `VARCHAR`, não nulo.
  - `description`: Descrição da disciplina, tipo `TEXT` ou `VARCHAR`.
  - `user_id`: Chave estrangeira para a tabela `users`, tipo `INTEGER`, não nulo.
  - `created_at`: Timestamp de criação, tipo `TIMESTAMP WITH TIME ZONE`.
  - `updated_at`: Timestamp de atualização, tipo `TIMESTAMP WITH TIME ZONE`.
  - `archived_at`: Timestamp para "soft delete" ou arquivamento, tipo `TIMESTAMP WITH TIME ZONE`, opcional.
- **Relacionamento**: Um usuário pode ter várias disciplinas, mas cada disciplina pertence a um único usuário (um-para-muitos).
- **Funcionalidade de Arquivamento**: As disciplinas poderão ser arquivadas (soft delete) em vez de serem excluídas permanentemente. Isso será controlado pelo campo `archived_at`.

## Risks / Trade-offs

- **Escolha do tipo de ID**: Usar `UUID` pode complicar um pouco as URLs e as consultas, mas evita a exposição de contagens de registros. Usar `INTEGER` é mais simples, mas menos seguro em alguns contextos. A decisão inicial será por `INTEGER` para simplicidade, podendo ser reavaliada se necessário.
