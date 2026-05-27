## Context

Hoje os dados acadêmicos só existem dentro do app Streamlit (consumindo Xano). Não há export — usuário não consegue arquivar/imprimir/backupar. A change adiciona uma página dedicada de exportação que reusa exatamente os endpoints já existentes (`subjects_search`, `tasks_list`).

Restrições do projeto (AGENTS.md / Regra Nº1):
- Sem CSS, sem `unsafe_allow_html=True` para estilo.
- Sem novos endpoints Xano (Regra Nº2 mantida — qualquer push manual).
- Página nativa Streamlit com componentes do Standard.

## Goals / Non-Goals

**Goals:**
- Exportar Tarefas, Disciplinas e Snapshot do Dashboard em CSV e PDF.
- Filtros úteis na exportação de Tarefas (disciplina, status, prioridade).
- Geração 100% client-side (in-memory) com `st.download_button` — sem servidor de arquivos, sem upload em lugar nenhum.
- Helpers puros em `lib/exporters.py` testáveis isoladamente.

**Non-Goals:**
- Agendar relatórios automáticos / e-mail.
- Exportar histórico de eventos / log_event do Xano.
- Edição/template customizado de PDF pelo usuário.
- XLSX (CSV + PDF já cobre o caso de uso).

## Decisions

### 1. Biblioteca PDF: `fpdf2`

**Escolha:** `fpdf2` (pacote `fpdf2` no PyPI, importado como `from fpdf import FPDF`).

**Por quê:**
- Leve (~200 KB), sem dependências nativas — instala limpo no Streamlit Cloud.
- API simples para tabelas e cabeçalhos, suficiente pro escopo.
- Suporte nativo a UTF-8 (acentos PT-BR) com fontes embutidas.

**Alternativas consideradas:**
- `reportlab`: mais poderoso, mas pesado e API mais verbosa pro escopo simples.
- `weasyprint`: requer libs nativas (Cairo/Pango), problemático em Streamlit Cloud.

### 2. CSV nativo (módulo `csv` da stdlib)

Sem dependência extra. Geração via `io.StringIO` → `bytes` → `st.download_button`. Delimitador `,` e encoding UTF-8 com BOM (`utf-8-sig`) pra abrir certinho no Excel pt-BR.

### 3. Estrutura de `lib/exporters.py`

Funções puras (sem Streamlit, sem I/O em disco):

```python
def tasks_to_csv(tasks: list[dict], subjects_by_id: dict[int, dict]) -> bytes
def tasks_to_pdf(tasks: list[dict], subjects_by_id: dict[int, dict], *, title: str) -> bytes
def subjects_to_csv(subjects: list[dict], tasks: list[dict]) -> bytes
def subjects_to_pdf(subjects: list[dict], tasks: list[dict], *, title: str) -> bytes
def dashboard_snapshot_to_pdf(subjects, tasks, *, today) -> bytes
def dashboard_snapshot_to_csv(subjects, tasks, *, today) -> bytes
```

Cada função retorna `bytes` — passa direto pro `data=` do `st.download_button`. Testáveis com `ast.parse` + chamadas com dados mock.

### 4. Filtros nos exports de Tarefas

Os 3 filtros (disciplina, status, prioridade) são aplicados via widgets na própria página (`st.selectbox` / `st.multiselect`). A lista filtrada é passada pros exporters. Sem filtros = exporta tudo.

### 5. Nome do arquivo

Padrão `edutrack_<tipo>_<YYYY-MM-DD>.<ext>` (ex.: `edutrack_tarefas_2026-05-25.csv`). Data via `_dt.date.today().isoformat()`.

### 6. Snapshot do Dashboard

Replica a lógica de `home.py` (métricas, progresso por disciplina, próximas 5 tarefas) mas via helpers já existentes em `lib/dashboard_utils.py` — sem duplicar regras. PDF tem cabeçalho com título "EduTrack AI — Resumo" + data de geração.

## Risks / Trade-offs

- **[Acentos no PDF]** → fpdf2 com fonte default (Helvetica) só cobre latin-1. Mitigação: usar fonte DejaVu (embutida no pacote) com `add_font("DejaVu", "", "DejaVuSans.ttf")` — funciona com acentos PT-BR.
- **[Tabelas longas no PDF]** → muitas tarefas podem estourar a página. Mitigação: fpdf2 quebra páginas automaticamente; usar `set_auto_page_break(auto=True, margin=15)`.
- **[CSV no Excel pt-BR]** → vírgula como separador decimal confunde. Mitigação: encoding `utf-8-sig` (BOM) e formatar % como inteiro sem casas (`50%` em vez de `0,5`).
- **[Memória pra exports muito grandes]** → 100% in-memory. Aceitável pro escopo de um estudante (centenas de tarefas, não milhares).
- **[Nova dependência]** → adiciona `fpdf2` ao `requirements.txt`. Trade-off aceito vs. não ter PDF.
