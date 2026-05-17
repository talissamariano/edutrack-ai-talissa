## 1. Configuração do Banco de Dados

- [x] 1.1 Criar um arquivo de migração para a nova tabela `subjects`.
- [x] 1.2 Definir o esquema da tabela `subjects` no arquivo de migração, incluindo as colunas `id`, `name`, `description`, `user_id`, `created_at`, e `updated_at`.
- [x] 1.3 Adicionar a coluna `archived_at` à tabela `subjects`.
- [x] 1.4 Adicionar a chave estrangeira `user_id` que referencia a tabela `users`.
- [x] 1.5 Executar a migração para criar a tabela no banco de dados.

## 2. Implementação da Lógica de Negócios

- [x] 2.1 Criar o modelo (Model) para a tabela `subjects`.
- [x] 2.2 Implementar a função para criar uma nova disciplina.
- [x] 2.3 Implementar a função para listar as disciplinas de um usuário, com opção para incluir arquivadas.
- [x] 2.4 Implementar a função para atualizar uma disciplina.
- [x] 2.5 Implementar a função para excluir uma disciplina.
- [x] 2.6 Implementar a função para arquivar uma disciplina.
- [x] 2.7 Implementar a função para desarquivar uma disciplina.
- [x] 2.8 Adicionar validações para garantir que os dados de entrada são válidos (ex: `name` não pode ser nulo).
- [x] 2.9 Adicionar verificações de permissão para garantir que um usuário só pode modificar suas próprias disciplinas.

## 3. Endpoints da API

- [x] 3.1 Criar o endpoint `POST /subjects` para criar uma nova disciplina.
- [x] 3.2 Criar o endpoint `GET /subjects` para listar as disciplinas do usuário autenticado.
- [x] 3.3 Criar o endpoint `PUT /subjects/:id` para atualizar uma disciplina.
- [x] 3.4 Criar o endpoint `DELETE /subjects/:id` para excluir uma disciplina.
- [x] 3.5 Criar o endpoint `POST /subjects/:id/archive` para arquivar uma disciplina.
- [x] 3.6 Criar o endpoint `POST /subjects/:id/unarchive` para desarquivar uma disciplina.

## 4. Testes

- [~] 4.1 Escrever testes de unidade para a lógica de negócios (funções de CRUD).
- [~] 4.2 Escrever testes de integração para os endpoints da API.
- [~] 4.3 Escrever testes para os cenários de erro e de permissão.

*NOTE: Testes foram pulados pois não foi identificado um framework de testes no projeto.*
