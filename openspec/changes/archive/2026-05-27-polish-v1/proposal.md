## Why

Dois itens da checklist v2 ainda estão incompletos: a exportação de tarefas não tem filtro temporal (dificultando relatórios por semestre/período), e a tela de login/cadastro é funcional mas visualmente básica — não transmite a identidade do app para quem chega pela primeira vez.

## What Changes

- **Relatórios — filtro por período**: adição de dois `st.date_input` ("De" / "Até") na seção Tarefas da página Relatórios; filtro aplicado em memória antes de chamar os exporters. Sem alterações nos exporters ou no Xano.
- **Login — layout mais atrativo**: refactor de `login.py` para usar colunas (col esquerda: marca + slogan + dicas; col direita: tabs com formulários), aproveitando o tema candy pastel já configurado. Sem CSS, sem `unsafe_allow_html`.

## Capabilities

### New Capabilities
<!-- nenhuma nova capability — são melhorias em capabilities existentes -->

### Modified Capabilities
- `reports-export`: seção Tarefas da página Relatórios passa a suportar filtro por período (data inicial + data final)
- `auth-module`: tela de login/cadastro tem layout aprimorado com colunas e seção de boas-vindas

## Impact

- Modificado: `pages/4_📊_Relatorios.py` (filtro de período)
- Modificado: `login.py` (layout em colunas)
- Sem alterações no Xano, sem novos arquivos, sem novas dependências Python
