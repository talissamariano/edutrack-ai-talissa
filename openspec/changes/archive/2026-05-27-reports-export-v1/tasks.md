## 1. Dependências

- [x] 1.1 Adicionar `fpdf2` ao `requirements.txt`
- [x] 1.2 Instalar localmente (`pip install fpdf2`) e validar import `from fpdf import FPDF`

## 2. Helpers de exportação (`lib/exporters.py`)

- [x] 2.1 Criar `lib/exporters.py` com função `tasks_to_csv(tasks, subjects_by_id) -> bytes` usando `csv.DictWriter` + `io.StringIO` + encoding `utf-8-sig`
- [x] 2.2 Implementar `subjects_to_csv(subjects, tasks) -> bytes` com colunas nome, professor, carga horária, semestre, % progresso, total, concluídas
- [x] 2.3 Implementar `dashboard_snapshot_to_csv(subjects, tasks, today) -> bytes` com seções separadas (Métricas, Progresso por disciplina, Próximas tarefas)
- [x] 2.4 Implementar `tasks_to_pdf(tasks, subjects_by_id, title) -> bytes` usando fpdf2 com `set_auto_page_break(auto=True, margin=15)` e fonte com suporte UTF-8
- [x] 2.5 Implementar `subjects_to_pdf(subjects, tasks, title) -> bytes`
- [x] 2.6 Implementar `dashboard_snapshot_to_pdf(subjects, tasks, today) -> bytes` com título "EduTrack AI — Resumo" e data
- [x] 2.7 Garantir que todas as funções são puras: não importam streamlit, não fazem I/O em disco, não chamam Xano

## 3. Página Relatórios (`pages/4_📊_Relatorios.py`)

- [x] 3.1 Criar `pages/4_📊_Relatorios.py` com `st.title("📊 Relatórios")` e carregamento de `subjects_search()` + `tasks_list()` com tratamento de `SessionExpired` (mesmo padrão das outras páginas)
- [x] 3.2 Seção **Tarefas**: filtros (`st.selectbox` disciplina com "Todas", `st.multiselect` status, `st.multiselect` prioridade); aplicar filtros em memória
- [x] 3.3 Seção **Tarefas**: dois `st.download_button` (CSV e PDF) com `file_name=f"edutrack_tarefas_{hoje.isoformat()}.{ext}"` e `mime` apropriado; mensagem "Nenhuma tarefa para exportar" quando lista vazia
- [x] 3.4 Seção **Disciplinas**: dois `st.download_button` (CSV e PDF) usando todas as disciplinas
- [x] 3.5 Seção **Snapshot do Dashboard**: dois `st.download_button` (CSV e PDF)
- [x] 3.6 Registrar a página em `app.py` no `st.navigation` (na ordem natural após Tarefas/Perfil)

## 4. Qualidade

- [x] 4.1 Sanidade Python (`ast.parse`) em `lib/exporters.py` e `pages/4_📊_Relatorios.py`
- [x] 4.2 Verificar ausência de `unsafe_allow_html=True` na nova página
- [x] 4.3 Smoke test manual: rodar `streamlit run app.py`, abrir Relatórios, baixar 6 arquivos (3 CSV + 3 PDF) e abrir cada um pra conferir conteúdo e acentos PT-BR
