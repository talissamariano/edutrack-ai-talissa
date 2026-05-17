## Why

Para permitir que os usuários gerenciem suas disciplinas acadêmicas, é necessário criar uma nova tabela no banco de dados para armazenar as informações das disciplinas. Isso fornecerá uma base para futuras funcionalidades, como controle de acesso e automações.

## What Changes

- Adicionar uma nova tabela `subjects` ao banco de dados.
- A tabela `subjects` terá um relacionamento com a tabela `users` para definir a propriedade.
- Os campos iniciais incluirão `name`, `description`, e `user_id`.
- A funcionalidade de arquivamento (soft delete) será incluída para permitir que os usuários ocultem disciplinas sem excluí-las permanentemente.

## Capabilities

### New Capabilities
- `subjects-db`: Gerenciamento do ciclo de vida das disciplinas no banco de dados, incluindo criação, leitura, atualização e exclusão (CRUD).

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

- **Banco de Dados**: Uma nova tabela `subjects` será adicionada.
- **API**: Novos endpoints podem ser necessários para gerenciar as disciplinas.
- **Frontend**: Novas visualizações podem ser necessárias para exibir e gerenciar as disciplinas.
