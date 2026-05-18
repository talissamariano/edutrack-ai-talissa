# subjects-search Specification

## Purpose

Define um endpoint de busca que permite ao usuário autenticado localizar suas disciplinas por nome ou pelas que possuem tarefas atrasadas.

## ADDED Requirements

### Requirement: Endpoint de busca autenticado e isolado por usuário

O sistema SHALL expor um endpoint de busca de `subjects` que exige autenticação (`auth = "user"`) e retorna apenas registros cujo `user_id` é igual ao do usuário autenticado.

#### Scenario: Busca sem autenticação é rejeitada

- **WHEN** a requisição ao endpoint de busca não possui token de usuário válido
- **THEN** o sistema rejeita a requisição como não autorizada

#### Scenario: Resultado restrito ao usuário

- **WHEN** um usuário autenticado executa a busca
- **THEN** o sistema retorna somente disciplinas com `user_id` igual ao do usuário autenticado

### Requirement: Filtro por nome

O sistema SHALL filtrar as disciplinas por correspondência textual no campo `name` quando um termo de busca for fornecido.

#### Scenario: Busca por nome

- **WHEN** o usuário informa um termo de nome existente em suas disciplinas
- **THEN** o sistema retorna as disciplinas do usuário cujo `name` corresponde ao termo

### Requirement: Filtro por tarefas atrasadas

O sistema SHALL permitir filtrar as disciplinas que possuem ao menos uma `academic_task` atrasada, onde atrasada significa `status != "done"` e `due_date < agora`.

#### Scenario: Busca por disciplinas com tarefas atrasadas

- **WHEN** o usuário solicita a busca por disciplinas com tarefas atrasadas
- **THEN** o sistema retorna apenas as disciplinas do usuário que têm pelo menos uma tarefa com `status != "done"` e `due_date` anterior ao momento atual

### Requirement: Combinação de filtros como OU

O sistema SHALL aplicar os filtros de nome e de tarefas atrasadas de forma combinada por OU quando ambos forem fornecidos.

#### Scenario: Ambos os filtros fornecidos

- **WHEN** o usuário informa um termo de nome e também solicita o filtro de tarefas atrasadas
- **THEN** o sistema retorna disciplinas que correspondem ao nome OU que possuem tarefas atrasadas
