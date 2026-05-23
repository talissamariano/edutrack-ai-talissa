# tasks-module Specification

## Purpose

Define o módulo de gestão de tarefas acadêmicas do EduTrack AI: cadastro, listagem, edição, exclusão, marcação de conclusão, filtros, agrupamento, sinalização de prazo vencido, calendário mensal e histórico de tarefas de disciplinas arquivadas. Todas as operações são restritas ao usuário autenticado.

## ADDED Requirements

### Requirement: Cadastro de tarefa vinculada a disciplina e usuário

O sistema SHALL permitir que o usuário autenticado cadastre uma tarefa informando `title` (obrigatório), `description`, `due_date`, `status` e `subject_id` de uma disciplina ativa do próprio usuário. O backend SHALL armazenar `user_id = $auth.id` e nunca confiar em input do cliente para o usuário.

#### Scenario: Cadastro bem-sucedido

- **WHEN** o usuário autenticado envia `title`, `subject_id` válidos e demais campos opcionais
- **THEN** o sistema cria a tarefa em `academic_tasks` vinculada ao `user_id` autenticado e ao `subject_id` informado

#### Scenario: Título vazio rejeitado

- **WHEN** o usuário envia uma tarefa sem `title` ou com `title` em branco
- **THEN** o sistema rejeita com erro de validação e não cria o registro

#### Scenario: Subject de outro usuário rejeitado

- **WHEN** o `subject_id` informado pertence a outro usuário
- **THEN** o sistema rejeita com erro de não autorizado e não cria a tarefa

### Requirement: Listagem com filtros e isolamento por usuário

O sistema SHALL listar somente as tarefas cujo `user_id` é igual ao usuário autenticado, com filtros opcionais por `subject_id`, `status` e `only_overdue`.

#### Scenario: Lista padrão

- **WHEN** o usuário autenticado consulta `GET /academic_tasks` sem filtros
- **THEN** o sistema retorna todas as tarefas do usuário

#### Scenario: Filtro por status

- **WHEN** o usuário consulta com `status=pending`
- **THEN** o sistema retorna apenas tarefas com `status` igual a `pending`

#### Scenario: Filtro por disciplina

- **WHEN** o usuário consulta com `subject_id` de uma disciplina sua
- **THEN** o sistema retorna apenas tarefas vinculadas a essa disciplina

#### Scenario: Filtro apenas atrasadas

- **WHEN** o usuário consulta com `only_overdue=true`
- **THEN** o sistema retorna apenas tarefas com `status != "done"` e `due_date < agora`

### Requirement: Edição de tarefa com ownership

O sistema SHALL permitir editar uma tarefa via `PATCH /academic_tasks/{id}` somente se ela pertence ao usuário autenticado.

#### Scenario: Edição válida

- **WHEN** o usuário edita campos de uma tarefa sua
- **THEN** o sistema atualiza o registro e retorna a versão nova

#### Scenario: Edição de tarefa de outro usuário

- **WHEN** o usuário tenta editar uma tarefa cujo `user_id` é de outro usuário
- **THEN** o sistema rejeita com erro de acesso negado

### Requirement: Exclusão de tarefa com confirmação

O sistema SHALL excluir uma tarefa via `DELETE /academic_tasks/{id}` somente se ela pertence ao usuário autenticado, e a interface SHALL exigir confirmação nativa antes de chamar o backend.

#### Scenario: Excluir com confirmação

- **WHEN** o usuário clica em excluir e confirma no diálogo
- **THEN** o sistema chama `DELETE /academic_tasks/{id}` e remove o registro

#### Scenario: Cancelar exclusão

- **WHEN** o usuário clica em excluir e escolhe "Cancelar" no diálogo
- **THEN** nenhuma chamada ao backend é feita e a tarefa permanece

### Requirement: Marcar tarefa como concluída

O sistema SHALL oferecer um atalho na linha da tarefa para mudar seu `status` para `"done"`, sem abrir um modal.

#### Scenario: Atalho de conclusão

- **WHEN** o usuário clica no botão `✓` de uma tarefa pendente
- **THEN** o sistema chama o endpoint correspondente e a tarefa passa a ter `status = "done"`

### Requirement: Filtros de status no frontend

A tela SHALL expor um filtro por status nos valores `pending`, `in_progress`, `done`, com display em PT-BR ("Pendente", "Em andamento", "Concluída").

#### Scenario: Filtragem por Em andamento

- **WHEN** o usuário seleciona "Em andamento" no filtro de status
- **THEN** a tela exibe somente tarefas com `status = "in_progress"`

### Requirement: Sinalização visual de prazo vencido

A tela SHALL sinalizar tarefas vencidas (`status != "done"` e `due_date < hoje`) com ícone `⚠️` antes do título e `due_date` exibido em destaque (`st.error` ou equivalente nativo), sem uso de CSS customizado.

#### Scenario: Renderização de tarefa atrasada

- **WHEN** uma tarefa não concluída tem `due_date` anterior ao dia atual
- **THEN** sua linha exibe `⚠️` antes do título e o prazo em destaque vermelho via componente nativo

### Requirement: Agrupamento por disciplina ou por urgência

A aba de listagem SHALL oferecer ao usuário a escolha entre agrupar as tarefas por disciplina ou por prazo. No modo por prazo, as tarefas SHALL ser agrupadas em seções de urgência (Atrasadas, Hoje, Esta semana, Próximas 2 semanas, Mais tarde, Sem prazo definido, Concluídas).

#### Scenario: Agrupar por disciplina

- **WHEN** o usuário seleciona "Agrupar por Disciplina"
- **THEN** as tarefas são exibidas em grupos por disciplina

#### Scenario: Agrupar por prazo com sinalização de urgência

- **WHEN** o usuário seleciona "Agrupar por Prazo"
- **THEN** as tarefas são exibidas em seções rotuladas como "🔴 Atrasadas", "🟠 Hoje", "🟡 Esta semana", "🟢 Próximas 2 semanas", "🔵 Mais tarde", "⚪ Sem prazo definido" e "✅ Concluídas"
- **AND** apenas as seções com pelo menos uma tarefa são exibidas

### Requirement: Histórico de tarefas de disciplinas arquivadas

A tela SHALL exibir uma aba dedicada para tarefas de disciplinas **arquivadas**, agrupadas por disciplina (subpastas via `st.expander`).

#### Scenario: Listagem no histórico

- **WHEN** o usuário abre a aba "📦 Histórico"
- **THEN** o sistema lista somente tarefas cujo `subject` está arquivado, agrupadas por disciplina

#### Scenario: Aba de ativas não exibe tarefas arquivadas

- **WHEN** o usuário está em "📋 Listar"
- **THEN** o sistema exibe somente tarefas de disciplinas ativas

### Requirement: Interface Standard sem CSS customizado

A página SHALL usar exclusivamente componentes nativos do Streamlit. Não SHALL utilizar `st.markdown(..., unsafe_allow_html=True)` para fins de estilo (uso permitido apenas para texto/markdown puro).

#### Scenario: Inspeção do código

- **WHEN** o código da página `pages/2_📝_Tarefas.py` é inspecionado
- **THEN** não há chamadas `unsafe_allow_html=True` com tags HTML/CSS injetadas para estilização
