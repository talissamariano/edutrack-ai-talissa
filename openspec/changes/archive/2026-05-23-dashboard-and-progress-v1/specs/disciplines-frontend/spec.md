# disciplines-frontend Specification (delta)

## ADDED Requirements

### Requirement: Progresso da disciplina na listagem

A listagem de disciplinas ativas SHALL exibir, para cada disciplina, a porcentagem de progresso calculada como `concluídas / total` das suas tarefas, em formato numérico e em barra visual (`st.progress`). Disciplinas sem tarefas SHALL exibir 0%.

#### Scenario: Disciplina com tarefas

- **WHEN** a disciplina tem tarefas associadas
- **THEN** a linha exibe o percentual (ex.: "60%") e a `st.progress` correspondente

#### Scenario: Disciplina sem tarefas

- **WHEN** a disciplina não tem nenhuma tarefa
- **THEN** a linha exibe "0%" e a `st.progress` em zero

### Requirement: Sinais de tarefas próximas e atrasadas na listagem

A listagem de disciplinas ativas SHALL exibir sinais textuais por linha quando houver tarefas pendentes em estados de atenção:
- `⚠️ N atrasada(s)` quando há tarefas com `status != "done"` e `due_date < hoje`.
- `📅 N próxima(s)` quando há tarefas com `status != "done"` e `due_date` entre hoje e hoje+7 dias.
Disciplinas sem nenhum desses estados NÃO SHALL exibir o sinal.

#### Scenario: Disciplina com tarefa atrasada

- **WHEN** a disciplina tem pelo menos uma tarefa atrasada
- **THEN** a linha exibe `⚠️ N atrasada(s)` com o número correspondente

#### Scenario: Disciplina com tarefa próxima (não atrasada)

- **WHEN** a disciplina tem pelo menos uma tarefa pendente com prazo entre hoje e hoje+7 dias
- **THEN** a linha exibe `📅 N próxima(s)` com o número correspondente

#### Scenario: Disciplina sem alertas

- **WHEN** a disciplina não tem tarefas atrasadas nem próximas
- **THEN** a linha não exibe nenhum sinal extra
