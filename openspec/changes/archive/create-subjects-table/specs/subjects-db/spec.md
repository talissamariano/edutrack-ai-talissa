## ADDED Requirements

### Requirement: Criar uma nova disciplina
O sistema DEVE permitir que um usuário crie uma nova disciplina.

#### Scenario: Criação de disciplina com sucesso
- **WHEN** um usuário autenticado envia uma requisição para criar uma disciplina com dados válidos (nome)
- **THEN** o sistema DEVE criar uma nova entrada na tabela `subjects` associada ao usuário e retornar uma confirmação de sucesso.

#### Scenario: Tentativa de criação de disciplina sem nome
- **WHEN** um usuário autenticado envia uma requisição para criar uma disciplina sem um nome
- **THEN** o sistema DEVE retornar um erro indicando que o nome é obrigatório.

### Requirement: Listar as disciplinas de um usuário
O sistema DEVE permitir que um usuário liste todas as suas disciplinas, com a opção de incluir as arquivadas.

#### Scenario: Listagem de disciplinas com sucesso
- **WHEN** um usuário autenticado solicita a lista de suas disciplinas
- **THEN** o sistema DEVE retornar uma lista de todas as disciplinas não arquivadas que pertencem a esse usuário.

#### Scenario: Listagem de disciplinas incluindo arquivadas
- **WHEN** um usuário autenticado solicita a lista de suas disciplinas com a opção de incluir as arquivadas
- **THEN** o sistema DEVE retornar uma lista de todas as disciplinas que pertencem a esse usuário, incluindo as arquivadas.

### Requirement: Atualizar uma disciplina
O sistema DEVE permitir que um usuário atualize os dados de uma de suas disciplinas.

#### Scenario: Atualização de disciplina com sucesso
- **WHEN** um usuário autenticado envia uma requisição para atualizar uma disciplina que lhe pertence com dados válidos
- **THEN** o sistema DEVE atualizar os dados da disciplina no banco de dados e retornar uma confirmação de sucesso.

#### Scenario: Tentativa de atualizar uma disciplina de outro usuário
- **WHEN** um usuário autenticado tenta atualizar uma disciplina que não lhe pertence
- **THEN** o sistema DEVE retornar um erro de permissão negada.

### Requirement: Excluir uma disciplina
O sistema DEVE permitir que um usuário exclua uma de suas disciplinas.

#### Scenario: Exclusão de disciplina com sucesso
- **WHEN** um usuário autenticado envia uma requisição para excluir uma disciplina que lhe pertence
- **THEN** o sistema DEVE remover a disciplina do banco de dados e retornar uma confirmação de sucesso.

#### Scenario: Tentativa de excluir uma disciplina de outro usuário
- **WHEN** um usuário autenticado tenta excluir uma disciplina que não lhe pertence
- **THEN** o sistema DEVE retornar um erro de permissão negada.

### Requirement: Arquivar uma disciplina
O sistema DEVE permitir que um usuário arquive uma de suas disciplinas.

#### Scenario: Arquivamento de disciplina com sucesso
- **WHEN** um usuário autenticado envia uma requisição para arquivar uma disciplina que lhe pertence
- **THEN** o sistema DEVE definir o timestamp `archived_at` da disciplina e retornar uma confirmação de sucesso.

#### Scenario: Tentativa de arquivar uma disciplina de outro usuário
- **WHEN** um usuário autenticado tenta arquivar uma disciplina que não lhe pertence
- **THEN** o sistema DEVE retornar um erro de permissão negada.

#### Scenario: Tentativa de arquivar uma disciplina já arquivada
- **WHEN** um usuário autenticado tenta arquivar uma disciplina que já está arquivada
- **THEN** o sistema DEVE retornar um erro indicando que a disciplina já está arquivada.

### Requirement: Desarquivar uma disciplina
O sistema DEVE permitir que um usuário desarquive uma de suas disciplinas.

#### Scenario: Desarquivamento de disciplina com sucesso
- **WHEN** um usuário autenticado envia uma requisição para desarquivar uma disciplina que lhe pertence
- **THEN** o sistema DEVE definir o timestamp `archived_at` da disciplina como nulo e retornar uma confirmação de sucesso.

#### Scenario: Tentativa de desarquivar uma disciplina de outro usuário
- **WHEN** um usuário autenticado tenta desarquivar uma disciplina que não lhe pertence
- **THEN** o sistema DEVE retornar um erro de permissão negada.

#### Scenario: Tentativa de desarquivar uma disciplina não arquivada
- **WHEN** um usuário autenticado tenta desarquivar uma disciplina que não está arquivada
- **THEN** o sistema DEVE retornar um erro indicando que a disciplina não está arquivada.
