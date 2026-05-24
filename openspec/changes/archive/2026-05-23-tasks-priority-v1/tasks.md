## 1. Schema e funções Xano

- [x] 1.1 Adicionar `text priority?` ao schema de `tables/837133_academic_tasks.xs`
- [x] 1.2 Atualizar `functions/academic_tasks/310161_create_task.xs` para aceitar `text priority?` e gravar em `db.add.data`
- [x] 1.3 Atualizar `functions/academic_tasks/310163_update_task.xs` para aceitar e gravar `priority`
- [x] 1.4 Atualizar `functions/academic_tasks/310162_list_tasks.xs` para aceitar `text priority?` no input (sem alterar branches do `conditional` — filtro será aplicado no frontend)

## 2. APIs Xano

- [x] 2.1 Atualizar `apis/academic_tasks/3894336_academic_tasks_POST.xs` para declarar `text priority?` e repassar à função
- [x] 2.2 Atualizar `apis/academic_tasks/3894337_academic_tasks_GET.xs` para declarar `text priority?` e repassar à função
- [x] 2.3 Atualizar `apis/academic_tasks/3894338_academic_tasks_id_PATCH.xs` para declarar `text priority?` e repassar à função

## 3. Helper Streamlit

- [x] 3.1 Estender `tasks_create` em `lib/xano_client.py` para aceitar `priority` (omitido do payload quando `None`)
- [x] 3.2 Estender `tasks_update` em `lib/xano_client.py` para aceitar `priority`
- [x] 3.3 Estender `tasks_list` em `lib/xano_client.py` para aceitar `priority` como query param

## 4. Tela de Tarefas

- [x] 4.1 Adicionar constantes `PRIORITY_LABELS`, `PRIORITY_OPTIONS_FORM` e `PRIORITY_CODE_BY_LABEL` em `pages/2_📝_Tarefas.py`
- [x] 4.2 Adicionar selectbox "Prioridade" no form de Nova Tarefa (default Média) e converter para canônico antes de chamar `tasks_create`
- [x] 4.3 Adicionar selectbox "Prioridade" no dialog Editar (pré-preenchido com o valor atual) e chamar `tasks_update` com o canônico
- [x] 4.4 Adicionar selectbox "Prioridade" na barra de filtros (Todas/Baixa/Média/Alta) e persistir em `st.session_state["task_filtro_priority_label"]`
- [x] 4.5 Aplicar filtro de prioridade client-side sobre `todas_tasks` quando diferente de "Todas"
- [x] 4.6 Atualizar `_render_task_row` para incluir uma coluna nova "Prioridade" com o badge (🟢/🟡/🔴/⚪) entre Status e os botões de ação
- [x] 4.7 Atualizar `_render_header_row` com a nova coluna

## 5. Qualidade

- [x] 5.1 Sanidade Python (`ast.parse`) em `pages/2_📝_Tarefas.py` e `lib/xano_client.py`
- [x] 5.2 Verificar ausência de `unsafe_allow_html=True` para estilo nos arquivos modificados
