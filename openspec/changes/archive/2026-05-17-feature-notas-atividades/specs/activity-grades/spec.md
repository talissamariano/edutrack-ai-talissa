# activity-grades Specification

## Purpose

Permitir que o professor autenticado lance a nota de um aluno em uma atividade específica, armazenando o registro associado ao professor.

## ADDED Requirements

### Requirement: Armazenar nota de atividade

O sistema SHALL armazenar a nota de um aluno em uma atividade específica, associando o registro ao `user_id` do professor autenticado.

#### Scenario: Nota é persistida

- **WHEN** o professor lança uma nota válida para um aluno em uma atividade
- **THEN** o sistema persiste um registro em `activity_grades` com `student_id`, `activity_id`, `grade` e o `user_id` do professor autenticado

### Requirement: Lançar nota via API POST

O sistema SHALL expor um endpoint `POST /activity_grades` que exige autenticação e cria uma nota para um aluno em uma atividade específica.

#### Scenario: Lançamento de nota com sucesso

- **WHEN** um professor autenticado envia `student_id`, `activity_id` e `grade` válidos para `POST /activity_grades`
- **THEN** o sistema cria o registro vinculado ao `user_id` do professor e retorna a nota criada

#### Scenario: Requisição sem autenticação

- **WHEN** a requisição para `POST /activity_grades` não possui token de autenticação válido
- **THEN** o sistema rejeita a requisição com erro de não autorizado e não cria nenhum registro

#### Scenario: Dados de entrada inválidos

- **WHEN** o professor envia uma requisição sem `student_id`, sem `activity_id` ou com `grade` fora do intervalo permitido
- **THEN** o sistema rejeita a requisição com erro de validação e não cria nenhum registro
