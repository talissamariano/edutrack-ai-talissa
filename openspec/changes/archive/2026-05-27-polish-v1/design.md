## Context

Ambas as melhorias são puramente frontend (Streamlit), sem tocar no Xano. A restrição principal do projeto é: zero CSS / zero `unsafe_allow_html=True` — tudo via componentes nativos e `.streamlit/config.toml` já configurado (candy pastel).

## Goals / Non-Goals

**Goals:**
- Filtro de período funcional em Relatórios > Tarefas (filtra `due_date` ou `created_at`).
- Tela de login com coluna de marca à esquerda e formulários à direita, dentro do Standard.

**Non-Goals:**
- Filtro de período nas seções Disciplinas ou Dashboard snapshot.
- Upload de imagem/logo customizada pelo usuário.
- Animações ou transições.
- Alterar fluxo de autenticação (apenas o visual do login.py).

## Decisions

### 1. Campo filtrado no período: `due_date`

Filtrar por `due_date` é o mais útil pra estudante ("tarefas com prazo em janeiro"). `created_at` seria metadado interno menos relevante. Tarefas sem `due_date` são excluídas quando o filtro está ativo.

### 2. Comportamento padrão do filtro

`date_from = None`, `date_to = None` → sem filtro (exporta tudo como antes). O usuário ativa o filtro via `st.toggle("Filtrar por período")` — só mostra os `date_input` quando ativado, evitando poluição visual.

### 3. Layout do login: `st.columns([1, 1])`

Coluna esquerda (marca):
- `st.title("🎓 EduTrack AI")`
- Slogan em `st.markdown`
- Lista de bullets com as features principais (`st.info` ou `st.markdown`)
- Rodapé discreto com versão/ano

Coluna direita (formulários):
- Tabs "Entrar" / "Cadastrar" / "Esqueci a senha" (igual ao atual, só reposicionado)

Em telas estreitas o Streamlit empilha as colunas automaticamente — sem quebrar mobile.

### 4. Sem imagem/banner

`st.image` requereria um arquivo de asset no repo — overhead desnecessário agora. O emoji `🎓` grande no título já dá identidade visual suficiente dentro do Standard.

## Risks / Trade-offs

- **[Filtro de período e tarefas sem prazo]** → Tarefas sem `due_date` desaparecem do export quando filtro está ativo. Mitigação: caption explicativo abaixo dos date_inputs.
- **[Layout colunas em tela pequena]** → Streamlit empilha colunas automaticamente; resultado aceitável sem CSS.
- **[Slogan em PT-BR hardcoded]** → Aceitável; não há i18n no projeto.
