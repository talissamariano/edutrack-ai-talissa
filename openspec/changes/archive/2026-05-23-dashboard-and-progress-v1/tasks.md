## 1. Helper de agregação (lib/)

- [x] 1.1 Adicionar utilitários puros em `lib/dashboard_utils.py`: `is_overdue(task, today)`, `is_upcoming(task, today, days=7)`, `subject_progress(tasks)` (envolve `calculate_progress` + `json.loads`)

## 2. Home / Dashboard

- [x] 2.1 Reescrever `home.py` carregando `subjects_search()` + `tasks_list()` uma vez por rerun
- [x] 2.2 Modo boas-vindas: se zero disciplinas, exibir mensagem amigável + `st.page_link` para Disciplinas
- [x] 2.3 Modo dashboard: 4 `st.metric` em `st.columns(4)` — disciplinas ativas, tarefas pendentes, atrasadas, % progresso
- [x] 2.4 Barra `st.progress` da % geral abaixo das métricas
- [x] 2.5 Seção "Próximas tarefas" com `st.dataframe` das 5 pendentes mais próximas (título, disciplina, prazo)
- [x] 2.6 Tratar `xano.SessionExpired` em todas as chamadas (mantém padrão das outras páginas)

## 3. Disciplinas — Progresso e Sinais

- [x] 3.1 Em `pages/1_📚_Disciplinas.py`, carregar `tasks_list()` em paralelo com `subjects_search()` e indexar por `subject_id`
- [x] 3.2 Ampliar colunas de `_render_active_row` para incluir Progresso (texto + `st.progress`) e Sinais (texto)
- [x] 3.3 Calcular % via `subject_progress(tasks_da_disciplina)` (helper) — exibir `f"{pct:.0f}%"`
- [x] 3.4 Calcular contagens de atrasadas (`due_date < hoje`) e próximas (`hoje..hoje+7`); exibir `⚠️ N atrasada(s)` e/ou `📅 N próxima(s)` quando >0; nada se zero
- [x] 3.5 Atualizar o cabeçalho de colunas correspondente

## 4. Qualidade

- [x] 4.1 Garantir zero `unsafe_allow_html=True` para estilo em `home.py` e `pages/1_📚_Disciplinas.py`
- [x] 4.2 Sanidade Python (`ast.parse`) em arquivos modificados
