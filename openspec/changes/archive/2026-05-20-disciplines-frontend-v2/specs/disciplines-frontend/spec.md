# disciplines-frontend Specification (delta v2)

## ADDED Requirements

### Requirement: Carga horária e semestre da disciplina

A tela SHALL permitir informar `workload_hours` (inteiro de horas) e `semester` (inteiro do período do curso) ao cadastrar/editar uma disciplina, e o backend SHALL persistir esses campos na tabela `subjects`.

#### Scenario: Cadastro com carga horária e semestre

- **WHEN** o usuário cadastra uma disciplina informando carga horária e semestre
- **THEN** o sistema persiste `workload_hours` e `semester` no registro vinculado ao `user_id` autenticado

#### Scenario: Cadastro sem carga horária ou semestre

- **WHEN** o usuário cadastra deixando carga horária e/ou semestre em branco
- **THEN** o sistema aceita o cadastro e armazena os campos não informados como nulos

#### Scenario: Edição atualiza carga horária e semestre

- **WHEN** o usuário edita uma disciplina alterando carga horária e/ou semestre
- **THEN** o sistema atualiza os campos correspondentes via `PATCH /subjects/{id}`

### Requirement: Arquivar e desarquivar disciplinas via UI

A tela SHALL oferecer ações de arquivar e desarquivar disciplinas do usuário autenticado, consumindo os endpoints existentes (`POST /subjects/{id}/archive` e `POST /subjects/{id}/unarchive`).

#### Scenario: Arquivar disciplina ativa

- **WHEN** o usuário clica em "Arquivar" em uma disciplina ativa
- **THEN** o sistema chama `POST /subjects/{id}/archive`, a disciplina some da aba de ativas e aparece na aba de arquivadas

#### Scenario: Desarquivar disciplina

- **WHEN** o usuário clica em "Desarquivar" em uma disciplina arquivada
- **THEN** o sistema chama `POST /subjects/{id}/unarchive` e a disciplina volta para a aba de ativas

### Requirement: Aba dedicada para disciplinas arquivadas

A tela SHALL exibir uma aba dedicada para disciplinas arquivadas, separada das ativas, e a aba de ativas NÃO SHALL exibir disciplinas arquivadas.

#### Scenario: Aba "Arquivadas" lista apenas arquivadas

- **WHEN** o usuário abre a aba "📦 Arquivadas"
- **THEN** o sistema lista somente as disciplinas do usuário com `archived_at` definido

#### Scenario: Aba "Listar ativas" oculta arquivadas

- **WHEN** o usuário está na aba "📋 Listar ativas"
- **THEN** o sistema lista somente as disciplinas do usuário com `archived_at == null`

### Requirement: Ações por linha (Editar / Arquivar / Excluir) na listagem

A listagem de disciplinas SHALL exibir cada disciplina como uma linha com colunas (`st.columns`), com botões de ação na própria linha — Editar, Arquivar/Desarquivar e Excluir — sem depender de `st.expander` para revelá-los.

#### Scenario: Botões aparecem ao lado dos dados

- **WHEN** uma disciplina é renderizada na listagem
- **THEN** os botões correspondentes (Editar, Arquivar/Desarquivar, Excluir) aparecem na mesma linha visual, ao lado das informações da disciplina
