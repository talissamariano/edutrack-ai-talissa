# auth-module Specification (delta)

## ADDED Requirements

### Requirement: Aniversário no perfil do usuário

O sistema SHALL permitir que o usuário autenticado registre opcionalmente sua data de aniversário (`birthday`), persistida na tabela `user` como `date birthday?`. Os endpoints `GET /auth/me` e `PATCH /auth/profile` SHALL contemplar esse campo (retornar e aceitar atualizar, respectivamente).

#### Scenario: Cadastrar aniversário pela primeira vez

- **WHEN** o usuário autenticado preenche o campo de aniversário no perfil e salva
- **THEN** o sistema persiste a data em `user.birthday` via `PATCH /auth/profile`

#### Scenario: Editar aniversário existente

- **WHEN** o usuário altera o aniversário e salva
- **THEN** o sistema atualiza `user.birthday` para o novo valor

#### Scenario: Sem aniversário cadastrado

- **WHEN** o usuário nunca cadastrou aniversário (campo nulo) e abre o perfil
- **THEN** o campo aparece vazio e o sistema não exibe nenhuma mensagem relacionada na Home
