# progress-calculation Specification

## Purpose

Define o comportamento de um utilitário Python que calcula a porcentagem de progresso (tarefas concluídas em relação ao total) e retorna o resultado em JSON.

## ADDED Requirements

### Requirement: Calcular porcentagem de progresso

O script SHALL calcular a porcentagem de progresso como `(concluídas / total) * 100`, considerando concluída toda tarefa com `status == "done"`.

#### Scenario: Cálculo com tarefas concluídas e pendentes

- **WHEN** o script recebe uma lista com 4 tarefas, sendo 1 com `status == "done"`
- **THEN** o resultado contém `total = 4`, `completed = 1` e `percentage = 25.0`

#### Scenario: Todas as tarefas concluídas

- **WHEN** todas as tarefas da entrada têm `status == "done"`
- **THEN** `percentage = 100.0`

### Requirement: Retornar resultado em JSON

O script SHALL retornar o resultado como JSON contendo `total`, `completed` e `percentage`.

#### Scenario: Saída em JSON válido

- **WHEN** o script conclui o cálculo
- **THEN** ele retorna uma string JSON válida com as chaves `total`, `completed` e `percentage`

### Requirement: Tratar lista vazia sem erro

O script SHALL tratar o caso de total igual a zero sem lançar exceção de divisão por zero.

#### Scenario: Nenhuma tarefa fornecida

- **WHEN** o script recebe uma lista vazia de tarefas
- **THEN** ele retorna `total = 0`, `completed = 0` e `percentage = 0.0` sem erro
