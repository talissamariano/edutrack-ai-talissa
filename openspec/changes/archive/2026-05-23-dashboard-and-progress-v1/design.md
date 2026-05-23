## Context

Após mergear `auth-module-v1`, `disciplines-frontend-v2` e `tasks-module-v1`, temos no backend Xano: CRUD completo de `subjects` e `academic_tasks`, ambos com isolamento por `user_id`. A Home é estática (zeros hardcoded), as Disciplinas não mostram progresso e o usuário novo cai numa tela vazia ao logar.

O professor pediu na revisão: dashboard, indicador de progresso por disciplina, sinal de tarefas próximas e tela de boas-vindas. Esta é a "1ª onda" — feita apenas com agregação no Streamlit, sem mexer no backend.

Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Tela Home útil pós-login com 4 indicadores + lista de próximas tarefas.
- Sinal e progresso por disciplina na listagem.
- Estado de boas-vindas amigável quando o usuário não tem dados.
- Reaproveitar [scripts/calculate_progress.py](scripts/calculate_progress.py) para a lógica de %.
- **Zero mudança no backend Xano.**

**Non-Goals:**
- Tema visual / identidade (Dark Modern + Poppins — Módulo F).
- Relatórios e exportação (Módulo E).
- Prioridade nas tarefas (Módulo D).
- Novos endpoints / migração de schema.
- Testes automatizados, push/deploy.

## Decisions

### Fontes de dados (uma chamada de cada)

A Home e o Disciplinas vão precisar das mesmas duas listas:
- `xano.subjects_search()` — todas as disciplinas do usuário (com `archived_at`)
- `xano.tasks_list()` — todas as tarefas do usuário

Tudo o resto (totais, próximas, sinais por disciplina) é **agregação client-side em Python**. Mantém o backend simples e zero novos endpoints.

### Definições compartilhadas

- **Hoje** = `datetime.date.today()`
- **Atrasada** = `status != "done"` **e** `due_date < hoje`
- **Próxima** = `status != "done"` **e** `hoje <= due_date <= hoje + 7 dias`
- **Pendente** = `status != "done"` (independente de prazo)
- **Progresso** = `concluídas / total`; se total = 0 → 0% (já tratado em `calculate_progress.py`)

### Home

Layout:
1. Se `len(subjects_ativas) == 0` **e** `len(todas_subjects) == 0` → tela de boas-vindas (mensagem + botão "Cadastrar primeira disciplina" via `st.page_link`).
2. Caso contrário, dashboard:
   - Linha de `st.metric` com 4 indicadores (`st.columns(4)`):
     - 📚 Disciplinas ativas — `len([s for s in subjects if not s.archived_at])`
     - 📝 Pendentes — `len([t for t in tasks if t.status != "done"])`
     - ⚠️ Atrasadas — pendentes com `due_date < hoje`
     - ✅ Progresso geral — usa `calculate_progress(tasks)` e parseia a `percentage` do JSON
   - `st.progress` da % geral logo abaixo da métrica.
   - Seção "Próximas tarefas" com `st.dataframe` (título, disciplina, prazo) das top-5 pendentes ordenadas por `due_date`.

### Disciplinas — colunas extras

A listagem ativa hoje usa colunas `[3, 3, 1, 1, 1, 1, 1]` (Nome / Professor / Carga / Sem. / Editar / Arquivar / Excluir). Vou estender para `[3, 2, 1, 1, 1, 2, 1, 1, 1]` adicionando **Progresso** (barra mini + texto) e **Sinais** (texto curto). Cabeçalho ajusta junto.

A função `_render_active_row(subject)` recebe agora um mapa `tasks_by_subject: dict[int, list[task]]` para calcular tudo client-side:
- `progresso = calculate_progress(tasks_da_disciplina)` (string JSON; parsea pra dict)
- `atrasadas = N` e `proximas = N`
- Renderiza `st.progress(percentual/100)` + `f"{percentual:.0f}%"`
- Renderiza texto: `"⚠️ N atrasada(s)"` se N > 0; `"📅 N próxima(s)"` se N > 0; ou vazio.

### Reuso do calculate_progress

Importação:
```python
from scripts.calculate_progress import calculate_progress
import json
...
result = json.loads(calculate_progress(tasks_da_disciplina))
percentage = result["percentage"]
```

Não vou alterar `scripts/calculate_progress.py` — usar como está.

### Idioma e segurança

- Documentação/UI em português; nomes técnicos em inglês.
- Toda contagem é do **próprio usuário** (já vem filtrada por `user_id` no backend).

## Risks / Trade-offs

- [N+1 chamadas evitado] → Faço **2 chamadas únicas** (subjects + tasks) e agrupo localmente. Performance OK até centenas de tarefas; revisitar se virar gargalo.
- [Cálculo client-side de "atrasada"] → Usa hora local do navegador → pode divergir de fuso do Xano em poucos minutos perto da meia-noite. Aceitável para v1.
- [`calculate_progress.py` retorna JSON string em vez de dict] → Solução: `json.loads(...)`. Tradeoff aceitável; o script foi planejado pra uso externo (CLI/serviço).
- [Mudança no contrato visual das Disciplinas] → Adicionar 2 colunas pode comprimir o layout em telas pequenas. Aceitável; Standard do Streamlit reorganiza.
- [Performance do rerun] → A Home faz 2 chamadas a cada rerun. Sem cache. Pode crescer; cache leve com `@st.cache_data(ttl=10)` é melhoria possível em v2.
