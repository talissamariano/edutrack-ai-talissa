# subjects-access-control Specification

## Purpose

Garante que todas as operações sobre `subjects` exigem um usuário autenticado e que cada usuário só pode acessar ou modificar os próprios registros.

## Requirements

### Requirement: Autenticação obrigatória em todos os endpoints de subjects

Todo endpoint de `subjects` (`POST`, `GET`, `PATCH`, `DELETE`, `archive`, `unarchive`) SHALL exigir um usuário autenticado (`auth = "user"`).

#### Scenario: Requisição sem autenticação é rejeitada

- **WHEN** uma requisição para qualquer endpoint de `subjects` não possui token de usuário válido
- **THEN** o sistema rejeita a requisição como não autorizada e não executa a operação

### Requirement: Isolamento de dados por usuário

Toda operação de leitura, atualização, exclusão, arquivamento ou desarquivamento SHALL restringir o acesso aos registros cujo `user_id` é igual ao do usuário autenticado.

#### Scenario: Listagem retorna apenas registros do usuário

- **WHEN** um usuário autenticado lista `subjects`
- **THEN** o sistema retorna somente os registros com `user_id` igual ao do usuário autenticado

#### Scenario: Operação sobre registro de outro usuário é negada

- **WHEN** um usuário autenticado tenta atualizar, excluir, arquivar ou desarquivar um `subject` cujo `user_id` é de outro usuário
- **THEN** o sistema nega a operação com erro de acesso negado e não altera o registro

#### Scenario: Criação vincula ao usuário autenticado

- **WHEN** um usuário autenticado cria um `subject`
- **THEN** o sistema grava o `user_id` a partir do usuário autenticado, nunca de entrada do cliente

### Requirement: Verbo de atualização em conformidade RESTful

O endpoint de atualização de `subjects` SHALL usar o verbo `PATCH` (`PATCH /subjects/{id}`), conforme o padrão RESTful do projeto.

#### Scenario: Atualização exposta via PATCH

- **WHEN** o endpoint de atualização de `subjects` é auditado
- **THEN** ele está exposto como `PATCH /subjects/{id}` (e não `PUT`)
