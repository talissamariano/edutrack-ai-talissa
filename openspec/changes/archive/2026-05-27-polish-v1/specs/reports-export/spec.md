# reports-export Specification (delta)

## MODIFIED Requirements

### Requirement: Exportação de Tarefas

O sistema SHALL permitir exportar a lista de tarefas do usuário autenticado em CSV e PDF, aplicando filtros opcionais por disciplina, status, prioridade **e período (data inicial e/ou data final sobre `due_date`)**. As colunas exportadas SHALL ser: título, disciplina, prazo (DD/MM/YYYY), status, prioridade, descrição.

#### Scenario: Exportar todas as tarefas em CSV

- **WHEN** o usuário clica em "Baixar CSV" na seção Tarefas sem nenhum filtro aplicado
- **THEN** o sistema gera um arquivo CSV (UTF-8 com BOM) com todas as tarefas do usuário e dispara o download via `st.download_button`

#### Scenario: Exportar tarefas filtradas em PDF

- **WHEN** o usuário aplica filtros (ex.: disciplina = "Cálculo I", status = "pending") e clica em "Baixar PDF"
- **THEN** o PDF gerado contém apenas as tarefas que satisfazem os filtros, com cabeçalho indicando a data de geração

#### Scenario: Exportar tarefas por período

- **WHEN** o usuário ativa o filtro de período e define data inicial e/ou data final, depois clica em "Baixar CSV" ou "Baixar PDF"
- **THEN** apenas tarefas com `due_date` dentro do intervalo são incluídas na exportação; tarefas sem `due_date` são excluídas quando o filtro está ativo

#### Scenario: Sem tarefas no escopo

- **WHEN** os filtros (incluindo período) resultam em zero tarefas
- **THEN** o sistema exibe uma mensagem "Nenhuma tarefa para exportar" e oculta os botões de download
