# reports-export Specification (delta)

## ADDED Requirements

### Requirement: Página Relatórios

O sistema SHALL expor uma página "Relatórios" no Streamlit (`pages/4_📊_Relatorios.py`) acessível ao usuário autenticado, contendo seções para exportar Tarefas, Disciplinas e Snapshot do Dashboard.

#### Scenario: Acesso autenticado

- **WHEN** o usuário autenticado abre a página Relatórios
- **THEN** o sistema exibe três seções (Tarefas, Disciplinas, Snapshot do Dashboard), cada uma com botões de download em CSV e PDF

#### Scenario: Acesso sem autenticação

- **WHEN** o usuário não autenticado tenta abrir a página Relatórios
- **THEN** o sistema redireciona/bloqueia exibindo a tela de login (comportamento padrão do app)

### Requirement: Exportação de Tarefas

O sistema SHALL permitir exportar a lista de tarefas do usuário autenticado em CSV e PDF, aplicando filtros opcionais por disciplina, status e prioridade. As colunas exportadas SHALL ser: título, disciplina, prazo (DD/MM/YYYY), status, prioridade, descrição.

#### Scenario: Exportar todas as tarefas em CSV

- **WHEN** o usuário clica em "Baixar CSV" na seção Tarefas sem nenhum filtro aplicado
- **THEN** o sistema gera um arquivo CSV (UTF-8 com BOM) com todas as tarefas do usuário e dispara o download via `st.download_button`

#### Scenario: Exportar tarefas filtradas em PDF

- **WHEN** o usuário aplica filtros (ex.: disciplina = "Cálculo I", status = "pending") e clica em "Baixar PDF"
- **THEN** o PDF gerado contém apenas as tarefas que satisfazem os filtros, com cabeçalho indicando a data de geração

#### Scenario: Sem tarefas no escopo

- **WHEN** os filtros resultam em zero tarefas
- **THEN** o sistema exibe uma mensagem "Nenhuma tarefa para exportar" e desabilita ou oculta os botões de download

### Requirement: Exportação de Disciplinas

O sistema SHALL permitir exportar a lista de disciplinas do usuário autenticado em CSV e PDF, com as colunas: nome, professor, carga horária, semestre, % progresso, total de tarefas, tarefas concluídas.

#### Scenario: Exportar disciplinas em CSV

- **WHEN** o usuário clica em "Baixar CSV" na seção Disciplinas
- **THEN** o sistema gera um CSV contendo todas as disciplinas (ativas e arquivadas) com as colunas definidas

#### Scenario: Exportar disciplinas em PDF

- **WHEN** o usuário clica em "Baixar PDF" na seção Disciplinas
- **THEN** o sistema gera um PDF tabular com as mesmas colunas e cabeçalho com data de geração

### Requirement: Snapshot do Dashboard

O sistema SHALL permitir exportar um snapshot consolidado do Dashboard em CSV e PDF, contendo: métricas agregadas (disciplinas ativas, tarefas pendentes, tarefas atrasadas, progresso geral %), progresso por disciplina, e próximas 5 tarefas.

#### Scenario: Snapshot em PDF

- **WHEN** o usuário clica em "Baixar PDF" na seção Snapshot do Dashboard
- **THEN** o sistema gera um PDF com título "EduTrack AI — Resumo", data, métricas, tabela de progresso por disciplina, e tabela de próximas tarefas

#### Scenario: Snapshot em CSV

- **WHEN** o usuário clica em "Baixar CSV" na seção Snapshot do Dashboard
- **THEN** o sistema gera um CSV com as mesmas seções organizadas sequencialmente (separadas por linhas em branco e cabeçalhos)

### Requirement: Escopo restrito ao usuário autenticado

A exportação SHALL conter exclusivamente dados do usuário autenticado, derivados de chamadas a `xano.subjects_search()` e `xano.tasks_list()` — sem acesso a dados de outros usuários e sem novos endpoints no Xano.

#### Scenario: Isolamento de dados

- **WHEN** a página Relatórios é carregada
- **THEN** todas as listas exportáveis vêm de chamadas autenticadas aos endpoints existentes e refletem apenas os registros do `auth.id` atual

### Requirement: Geração sem CSS customizado

A página Relatórios SHALL usar exclusivamente componentes nativos do Streamlit (`st.subheader`, `st.selectbox`, `st.multiselect`, `st.download_button`, `st.info`, `st.markdown` apenas para texto). NÃO SHALL utilizar `st.markdown(..., unsafe_allow_html=True)` para estilo.

#### Scenario: Inspeção do código

- **WHEN** o código de `pages/4_📊_Relatorios.py` é inspecionado
- **THEN** não há chamadas a `unsafe_allow_html=True` com HTML/CSS para estilo

### Requirement: Helpers puros de exportação

O sistema SHALL prover funções puras em `lib/exporters.py` que recebem listas de dicts e retornam `bytes` (CSV ou PDF), sem dependência de Streamlit, sem I/O em disco, e sem chamadas de rede.

#### Scenario: Helpers testáveis isoladamente

- **WHEN** as funções de `lib/exporters.py` são chamadas com dados mock em um teste/script
- **THEN** retornam `bytes` válidos sem efeitos colaterais (não escrevem em disco, não chamam Xano)
