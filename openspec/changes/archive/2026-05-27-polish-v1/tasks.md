## 1. Relatórios — filtro por período

- [x] 1.1 Em `pages/4_📊_Relatorios.py`, adicionar `st.toggle("Filtrar por período")` antes dos botões de download da seção Tarefas
- [x] 1.2 Quando o toggle estiver ativo, exibir dois `st.date_input` lado a lado ("De" e "Até") com `value=None` como padrão
- [x] 1.3 Aplicar o filtro de período em memória sobre `tasks_filt`: excluir tarefas sem `due_date` e manter apenas as com `due_date` dentro do intervalo `[date_from, date_to]` (bordas inclusivas, respeitando campos None)
- [x] 1.4 Exibir `st.caption` explicativo abaixo dos date_inputs: "Tarefas sem prazo definido são excluídas quando o filtro está ativo."
- [x] 1.5 Sanidade `ast.parse` em `pages/4_📊_Relatorios.py`

## 2. Login — layout em colunas

- [x] 2.1 Refatorar `login.py` para usar `st.columns([1.1, 1])` — coluna esquerda com identidade visual, coluna direita com os formulários
- [x] 2.2 Coluna esquerda: `st.title("🎓 EduTrack AI")`, `st.markdown` com slogan (ex.: "Organize sua vida acadêmica."), `st.info` com lista de funcionalidades do app (disciplinas, tarefas, progresso, relatórios)
- [x] 2.3 Coluna direita: mover as tabs "Entrar" / "Cadastrar" / "Esqueci a senha" com seus formulários para dentro da coluna direita (conteúdo idêntico ao atual)
- [x] 2.4 Remover o `st.title` e `st.info` que estão no topo global do `login.py` atual (substituídos pela coluna esquerda)
- [x] 2.5 Sanidade `ast.parse` em `login.py` e verificar ausência de `unsafe_allow_html=True`

## 3. Qualidade

- [x] 3.1 Smoke test manual: abrir tela de login (verificar colunas), ir em Relatórios > Tarefas, ativar filtro de período, filtrar e baixar CSV/PDF
