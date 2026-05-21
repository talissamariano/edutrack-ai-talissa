## 1. Schema e funções Xano

- [x] 1.1 Adicionar `int workload_hours?` e `int semester?` ao schema da tabela `subjects` em `tables/837132_subjects.xs`
- [x] 1.2 Atualizar `functions/subjects/310154_create_subject.xs` para aceitar `int workload_hours?` e `int semester?` e persistir em `db.add.data`
- [x] 1.3 Atualizar `functions/subjects/310156_update_subject.xs` para aceitar e gravar `workload_hours` e `semester`

## 2. APIs Xano

- [x] 2.1 Atualizar `apis/subjects/3894328_subjects_POST.xs` para declarar `int workload_hours?` e `int semester?` e repassar à função
- [x] 2.2 Atualizar `apis/subjects/3894330_subjects_id_PATCH.xs` para declarar e repassar `workload_hours` e `semester`

## 3. Helper Streamlit

- [x] 3.1 Estender `subjects_create` e `subjects_update` em `lib/xano_client.py` aceitando `workload_hours` e `semester` (omitidos do payload quando `None`)
- [x] 3.2 Adicionar `subjects_archive(subject_id)` chamando `POST /subjects/{id}/archive`
- [x] 3.3 Adicionar `subjects_unarchive(subject_id)` chamando `POST /subjects/{id}/unarchive`

## 4. Tela de Disciplinas

- [x] 4.1 Reescrever `pages/1_📚_Disciplinas.py` com 3 abas: "📋 Listar ativas", "➕ Nova Disciplina", "📦 Arquivadas"
- [x] 4.2 Form Nova: adicionar campos `workload_hours` (`st.number_input`) e `semester` (`st.number_input`)
- [x] 4.3 Listagem ativas: trocar `st.dataframe`+`st.expander` por uma linha por disciplina via `st.container(border=True)` + `st.columns`, com Nome/Professor/Carga/Semestre + botões Editar/Arquivar/Excluir
- [x] 4.4 Listagem arquivadas: mesma estrutura com botões Desarquivar/Excluir
- [x] 4.5 Edit dialog (`@st.dialog`): incluir campos `workload_hours` e `semester` pré-preenchidos
- [x] 4.6 Implementar ação Arquivar (chama `subjects_archive` + flash + rerun)
- [x] 4.7 Implementar ação Desarquivar (chama `subjects_unarchive` + flash + rerun)
- [x] 4.8 Split client-side ativas vs arquivadas via campo `archived_at` da resposta
- [x] 4.9 Manter confirmação nativa (`st.dialog`) para Excluir e tratamento de `SessionExpired`
- [x] 4.10 Verificar que a página continua sem `unsafe_allow_html` para estilo
