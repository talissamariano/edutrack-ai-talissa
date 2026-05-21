# Change: disciplines-frontend-v2

## Why

A v1 entregou listar/criar/editar/excluir/buscar de `subjects`. Faltam: campo de **carga horária** (pedido obrigatório do checklist), **semestre do curso** para o aluno organizar disciplinas por período, fluxo completo de **arquivar/desarquivar** disciplinas no final do semestre, e um **layout** com ações por linha (Editar/Arquivar/Excluir) em vez de expanders separados.

## What Changes

Escopo estritamente limitado:

1. **Schema:** adicionar `workload_hours` (int) e `semester` (int do período do curso, ex.: 1, 2, 3) na tabela `subjects`.
2. **Backend Xano:**
   - `create_subject` aceita e persiste `workload_hours` + `semester` (opcionais).
   - `update_subject` aceita e atualiza `workload_hours` + `semester` (opcionais).
   - APIs `POST /subjects` e `PATCH /subjects/{id}` declaram e repassam os novos inputs.
   - `archive` / `unarchive` (já existentes) **não mudam**.
3. **Helper Streamlit:** `subjects_create` / `subjects_update` aceitam os novos campos; adicionar `subjects_archive(id)` e `subjects_unarchive(id)`.
4. **Frontend (`pages/1_📚_Disciplinas.py`) reescrita:**
   - 3 abas: **📋 Listar ativas**, **➕ Nova Disciplina**, **📦 Arquivadas**.
   - Form de Nova: nome, professor, carga horária, semestre, descrição.
   - Listagem ativa: uma linha por disciplina via `st.columns` com Nome/Professor/Carga/Semestre + botões **Editar**, **Arquivar**, **Excluir** na própria linha (sem expander).
   - Listagem arquivadas: mesma estrutura com botões **Desarquivar** e **Excluir**.
   - Edit dialog inclui os novos campos.
   - Confirmação nativa (`st.dialog`) para Excluir mantida.
   - Barra de busca por nome + checkbox "atrasadas" continua acima das abas; aplica em ambas ativas e arquivadas.
   - Split ativas vs arquivadas é client-side via campo `archived_at`.

Fora de escopo: visual/tema, paginação/ordenação avançada, integração com Tarefas, testes automatizados, push/deploy.

## Capabilities

### New Capabilities
<!-- Nenhuma capability nova; v2 expande disciplines-frontend existente. -->

### Modified Capabilities
- `disciplines-frontend`: adiciona requisitos de carga horária, semestre, arquivamento/desarquivamento via UI, e layout com ações por linha.

## Impact

- **Backend Xano:**
  - [tables/837132_subjects.xs](tables/837132_subjects.xs) — `workload_hours` (int?) e `semester` (int?)
  - [functions/subjects/310154_create_subject.xs](functions/subjects/310154_create_subject.xs) — novos inputs
  - [functions/subjects/310156_update_subject.xs](functions/subjects/310156_update_subject.xs) — novos inputs
  - [apis/subjects/3894328_subjects_POST.xs](apis/subjects/3894328_subjects_POST.xs) — declarar/repassar
  - [apis/subjects/3894330_subjects_id_PATCH.xs](apis/subjects/3894330_subjects_id_PATCH.xs) — declarar/repassar
- **Helper:** [lib/xano_client.py](lib/xano_client.py)
- **Frontend:** [pages/1_📚_Disciplinas.py](pages/1_📚_Disciplinas.py) — reescrita
- **Sem push/deploy** (Regra Nº2).
