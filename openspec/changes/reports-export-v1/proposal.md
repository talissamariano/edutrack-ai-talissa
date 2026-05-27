## Why

A usuária precisa levar/arquivar seus dados acadêmicos pra fora do EduTrack (planilha, impressão, backup pessoal). Hoje não existe nenhuma forma de exportar — só visualizar dentro do app.

## What Changes

- Nova página **Relatórios** com 3 blocos de exportação:
  - **Tarefas**: lista completa com filtros (disciplina, status, prioridade) e colunas título/disciplina/prazo/status/prioridade/descrição.
  - **Disciplinas**: nome, professor, carga horária, semestre, % progresso, total/concluídas.
  - **Snapshot do Dashboard**: métricas agregadas + progresso por disciplina + próximas 5 tarefas.
- Cada bloco oferece download em **CSV** e **PDF**.
- Downloads via `st.download_button` (componente nativo Streamlit).
- Sem alterações no backend Xano — só consome endpoints existentes (`subjects_search`, `tasks_list`).
- Sem CSS / sem `unsafe_allow_html` (Standard preservado).

## Capabilities

### New Capabilities
- `reports-export`: regras para a página Relatórios — quais conjuntos de dados são exportáveis, em quais formatos, com quais filtros, e garantias de escopo (somente dados do usuário autenticado).

### Modified Capabilities
<!-- nenhuma -->

## Impact

- Novo arquivo: `pages/4_📊_Relatorios.py`
- Novo módulo helper: `lib/exporters.py` (funções puras para gerar CSV e PDF a partir de listas)
- Nova dependência Python: `reportlab` (ou `fpdf2`) para PDF — decisão final no design
- Atualização de `requirements.txt`
- Sem mudanças em Xano, sem mudanças em outras páginas
