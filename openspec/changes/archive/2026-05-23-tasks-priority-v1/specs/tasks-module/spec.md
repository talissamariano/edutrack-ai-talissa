# tasks-module Specification (delta)

## ADDED Requirements

### Requirement: Prioridade da tarefa

O sistema SHALL aceitar opcionalmente o campo `priority` em cada tarefa, com valores canônicos `"low"`, `"medium"` ou `"high"`. O backend SHALL persistir esse valor e o frontend SHALL exibi-lo com rótulos em PT-BR ("Baixa", "Média", "Alta").

#### Scenario: Cadastro com prioridade

- **WHEN** o usuário cadastra uma tarefa selecionando uma prioridade
- **THEN** o sistema persiste o valor canônico correspondente em `priority`

#### Scenario: Cadastro sem prioridade (compatibilidade)

- **WHEN** o usuário cadastra uma tarefa sem selecionar prioridade
- **THEN** o sistema aceita o cadastro e armazena `priority` como nulo

#### Scenario: Edição altera prioridade

- **WHEN** o usuário edita uma tarefa alterando o valor de prioridade
- **THEN** o sistema atualiza o campo `priority` via `PATCH /academic_tasks/{id}`

### Requirement: Filtro por prioridade

A tela de Tarefas SHALL expor um filtro por prioridade na barra de filtros, com opções "Todas", "Baixa", "Média" e "Alta". Quando uma prioridade específica é selecionada, a listagem SHALL exibir somente tarefas com `priority` igual ao valor canônico correspondente.

#### Scenario: Filtragem por Alta

- **WHEN** o usuário seleciona "Alta" no filtro de prioridade
- **THEN** a tela exibe somente as tarefas cujo `priority` é `"high"`

#### Scenario: Filtro "Todas"

- **WHEN** o usuário mantém "Todas" no filtro de prioridade
- **THEN** o filtro de prioridade não restringe a listagem

### Requirement: Sinalização visual de prioridade

A linha de cada tarefa na listagem SHALL exibir um badge visual da prioridade, usando apenas componentes nativos do Streamlit (texto + emoji):
- 🟢 Baixa
- 🟡 Média
- 🔴 Alta
- ⚪ Sem prioridade (quando `priority` é nulo)

#### Scenario: Tarefa com prioridade Alta

- **WHEN** uma tarefa com `priority = "high"` é renderizada
- **THEN** a linha exibe "🔴 Alta" como rótulo da prioridade

#### Scenario: Tarefa sem prioridade (legacy)

- **WHEN** uma tarefa com `priority` nulo é renderizada
- **THEN** a linha exibe "⚪ Sem prioridade"
