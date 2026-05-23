# home-dashboard Specification

## Purpose

Define a tela inicial (Home) exibida ao usuário autenticado, com métricas agregadas (disciplinas ativas, tarefas pendentes/atrasadas, próximas tarefas e % de progresso) e um modo de boas-vindas para usuários sem dados.

## Requirements

### Requirement: Métricas agregadas no Dashboard

A Home SHALL exibir, para o usuário autenticado, métricas calculadas a partir dos seus próprios dados:
- Total de disciplinas ativas (não arquivadas).
- Total de tarefas pendentes (`status != "done"`).
- Total de tarefas atrasadas (`status != "done"` e `due_date < hoje`).
- Porcentagem de progresso geral, computada como `concluídas / total` usando o utilitário `scripts/calculate_progress.py`.

#### Scenario: Usuário com dados visualiza métricas

- **WHEN** o usuário autenticado abre a Home e possui pelo menos uma disciplina cadastrada
- **THEN** o sistema exibe quatro indicadores: disciplinas ativas, tarefas pendentes, tarefas atrasadas e percentual de progresso geral

### Requirement: Próximas tarefas

A Home SHALL exibir as próximas 5 tarefas do usuário, ordenadas por `due_date` ascendente, considerando apenas tarefas com `status != "done"`.

#### Scenario: Próximas tarefas listadas

- **WHEN** o usuário autenticado tem ao menos uma tarefa pendente
- **THEN** a Home exibe uma lista compacta das próximas 5 tarefas (ou todas, se houver menos), mostrando título, disciplina e prazo

#### Scenario: Sem tarefas pendentes

- **WHEN** o usuário autenticado não tem nenhuma tarefa pendente
- **THEN** a Home exibe uma mensagem positiva no lugar da lista (ex.: "🎉 Nenhuma tarefa pendente.")

### Requirement: Boas-vindas para usuário sem dados

Quando o usuário autenticado não possui **nenhuma disciplina** (ativa ou arquivada), a Home SHALL exibir uma tela de boas-vindas com explicação curta e um CTA para criar a primeira disciplina.

#### Scenario: Primeiro acesso (sem disciplinas)

- **WHEN** o usuário autenticado abre a Home e não tem nenhuma disciplina cadastrada
- **THEN** a Home exibe uma mensagem amigável e um botão/CTA que leva à página de Disciplinas
- **AND** as métricas e a lista de próximas tarefas NÃO são exibidas

### Requirement: Interface Standard sem CSS customizado

A página Home SHALL utilizar exclusivamente componentes nativos do Streamlit (`st.metric`, `st.progress`, `st.columns`, `st.container`, `st.button`, `st.dataframe`, `st.markdown` apenas para texto/markdown). Não SHALL utilizar `st.markdown(..., unsafe_allow_html=True)` para fins de estilização.

#### Scenario: Inspeção do código

- **WHEN** o código da Home é inspecionado
- **THEN** não há chamadas a `unsafe_allow_html=True` com tags HTML/CSS para estilo
