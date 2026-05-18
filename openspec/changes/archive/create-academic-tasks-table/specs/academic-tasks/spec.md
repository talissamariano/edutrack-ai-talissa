# academic-tasks Specification

## Purpose

Define a estrutura de banco de dados para o aluno registrar e gerenciar suas obrigações acadêmicas (lições, provas, trabalhos), vinculadas a uma disciplina e ao próprio aluno.

## ADDED Requirements

### Requirement: Criar tabela academic_tasks

O sistema SHALL armazenar obrigações acadêmicas em uma tabela `academic_tasks`, com os campos `title`, `description`, `due_date`, `status`, `subject_id` (referência a `subjects`) e `user_id` (referência ao aluno autenticado), além de campos de auditoria.

#### Scenario: Aluno registra uma obrigação acadêmica

- **WHEN** um aluno autenticado registra uma obrigação acadêmica para uma de suas disciplinas
- **THEN** o sistema persiste um registro em `academic_tasks` com `title`, `description`, `due_date`, `status`, `subject_id` e o `user_id` do aluno autenticado

### Requirement: Vínculo da obrigação à disciplina e ao aluno

O sistema SHALL associar cada obrigação acadêmica a uma disciplina via `subject_id` e ao aluno via `user_id`.

#### Scenario: Obrigação vinculada a uma disciplina

- **WHEN** uma obrigação acadêmica é criada com um `subject_id`
- **THEN** o registro referencia a disciplina correspondente na tabela `subjects`

#### Scenario: Obrigação pertence ao aluno autenticado

- **WHEN** uma obrigação acadêmica é criada
- **THEN** o registro armazena o `user_id` do aluno autenticado, permitindo filtrar obrigações por aluno
