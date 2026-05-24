## Context

Após `tasks-module-v1`, temos `academic_tasks` no Xano com campos: `id`, `title`, `description`, `due_date`, `status`, `subject_id`, `user_id`, `created_at`, `updated_at`, `archived_at`. A página de Tarefas tem 3 abas (Listar / Nova / Histórico) com filtros por título, status e atrasadas.

O professor pediu **prioridade** como campo adicional. Esta é a Onda 2, Módulo D. Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Adicionar `priority` (opcional) em `academic_tasks` sem quebrar tarefas existentes.
- UI completa: criação, edição, filtro e exibição visual.
- Manter Standard estrito (componentes nativos, sem CSS injetado).

**Non-Goals:**
- Ordenação automática por prioridade (continua sendo por prazo).
- Migração obrigatória de tarefas antigas (ficam como `null` → exibe "⚪ Sem prioridade").
- Relatórios/exportação (Módulo E).
- Tema visual (Módulo F).
- Testes automatizados, push/deploy.

## Decisions

### Schema

- **`text priority?`** na tabela `academic_tasks` — opcional, sem default no banco. Valores válidos pela aplicação: `"low"` / `"medium"` / `"high"`.
  - *Alternativa considerada:* usar `enum` no XanoScript — descartada para manter consistência com `status` (também text) e evitar alteração de schema mais rígida.

### Backend

- **`create_task`** ganha `text priority?` no input e grava em `db.add.data`. Sem precondition (qualquer valor de texto entra; UI controla os 3 valores válidos).
- **`update_task`** ganha `text priority?` no input e inclui em `db.edit.data`.
- **`list_tasks`** ganha `text priority?` no input. A combinação de filtros já existente (`subject_id`, `status`, `only_overdue`) sobe de 3 para 4 dimensões → seria 2⁴ = 16 branches no `conditional` de hoje. **Decisão pragmática:** mantemos as 8 branches atuais e **aplicamos o filtro de prioridade no frontend (client-side)** quando enviado. O backend ignora o param `priority` por enquanto.
  - *Alternativa:* refatorar `list_tasks` para 16 branches → descartada por complexidade.
  - *Trade-off:* o frontend recebe todas as tarefas (do conjunto já filtrado por outros critérios) e filtra `priority` em Python. Custo desprezível dado o volume típico.
- **API POST/PATCH/GET:** declaram `text priority?` e repassam à função. POST/PATCH usam o valor; GET pode aceitar e ignorar (para manter contrato consistente).
- **Sintaxe XanoScript:** apenas operadores validados em produção. Nenhuma novidade aqui — só adicionar campo.

### Helper Streamlit

- `tasks_create(..., priority=None)` — omite do payload quando `None`.
- `tasks_update(..., priority=None)` — mesma lógica.
- `tasks_list(..., priority=None)` — envia como param se fornecido (mesmo que backend ignore por enquanto).

### Frontend

- **Form Nova:** `st.selectbox("Prioridade", ["Baixa", "Média", "Alta"], index=1)` (default Média). Mapeia label → canônico (`"low"`/`"medium"`/`"high"`).
- **Dialog Editar:** mesmo selectbox; calcula `index` a partir do valor atual da tarefa.
- **Filtro:** novo `st.selectbox("Prioridade", ["Todas", "Baixa", "Média", "Alta"], index=0)` na barra de filtros. Selecionado "Todas" → não filtra. Caso contrário, filtra `tasks` client-side por `priority == canônico_correspondente`.
- **Badge na linha:** nova coluna (ou texto adjacente) com `🟢 Baixa` / `🟡 Média` / `🔴 Alta` / `⚪ Sem prioridade`. Vou adicionar uma **nova coluna** ao `st.columns` de `_render_task_row` antes dos botões.

#### Layout atual da linha

```
[5, 3, 2, 2, 1, 1, 1] = Título / Disciplina / Prazo / Status / ✓ / ✏️ / 🗑️
```

#### Layout novo (adiciona Prioridade entre Status e os botões)

```
[5, 3, 2, 2, 2, 1, 1, 1] = Título / Disciplina / Prazo / Status / Prioridade / ✓ / ✏️ / 🗑️
```

Cabeçalho do `_render_header_row` ajustado proporcionalmente.

### Mapeamento de valores (constantes em `pages/2_📝_Tarefas.py`)

```python
PRIORITY_LABELS = {"low": "🟢 Baixa", "medium": "🟡 Média", "high": "🔴 Alta"}
PRIORITY_OPTIONS_FORM = ["Baixa", "Média", "Alta"]
PRIORITY_CODE_BY_LABEL = {"Baixa": "low", "Média": "medium", "Alta": "high"}
```

### Idioma e segurança

- Documentação/UI em português; valores canônicos em inglês (snake_case/lowercase) no DB.
- Sem mudança de regra de ownership — backend continua filtrando por `user_id`.

## Risks / Trade-offs

- [Schema migration] → Campo opcional, sem perda de dados. Xano emite aviso de "data loss" no push de tabela (já vimos esse padrão antes); seguro confirmar.
- [Filtro de prioridade client-side] → Trade-off entre simplicidade do `list_tasks` (8 branches) vs. eficiência. Aceitável para v1.
- [Compatibilidade com tarefas antigas] → Sem default no DB; UI mostra "⚪ Sem prioridade" para `null`. Sem migração massiva.
- [Layout da linha mais largo] → Adiciona 1 coluna; em telas pequenas pode comprimir. Aceitável; `st.columns` reorganiza.
