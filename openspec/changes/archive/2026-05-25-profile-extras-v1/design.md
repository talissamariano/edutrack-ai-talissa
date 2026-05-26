## Context

A Home hoje tem dashboard (métricas, gráfico de barras horizontal, próximas tarefas) e tela de boas-vindas. O Perfil permite editar nome e e-mail. Backend tem auth-module com `GET /auth/me` e `PATCH /auth/profile`. Esta change adiciona "firula" pessoal — aniversário + frase do dia — sem mudar nada estrutural.

Entrega limitada à geração de arquivos (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Persistir aniversário do usuário e exibi-lo na edição do perfil.
- Exibir banner de parabéns na Home quando hoje for o aniversário.
- Mostrar uma frase do dia (pt-BR) consistente ao longo do dia.

**Non-Goals:**
- Gestão de semestre / auto-arquivar (Change B `semester-management`).
- Notificações por e-mail.
- Tema visual / Dark Modern (Onda visual).
- Chamadas de API externas (Quotable / ZenQuotes).
- Testes automatizados, push/deploy.

## Decisions

### Schema

- `date birthday?` na tabela `user` — opcional, sem default. Padrão Xano de campos opcionais; consistente com o que já fizemos em `subjects.archived_at` e similares.

### Backend Xano

- **`GET /auth/me`** — adicionar `"birthday"` à lista `output` do `db.get user`. Sem outras alterações.
- **`PATCH /auth/profile`** — adicionar `date birthday?` no `input` e incluir `birthday: $input.birthday` no `data` do `db.edit user`. Tarefas antigas (sem birthday) continuam funcionando — é opcional.
- Sintaxe XanoScript: somente operadores já validados em produção; sem novidade.

### Helper Streamlit

- `update_profile(*, name=None, email=None, birthday=None)` — adiciona `birthday` opcional. Quando informado como `datetime.date`, envia ISO (`YYYY-MM-DD`); quando `None`, omite do payload.
- `me()` retorna naturalmente o novo campo (Xano envia o que o output do `auth/me` definir).

### Quotes (lib/quotes.py)

- Lista `QUOTES: list[dict]` com 100 itens. Estrutura por item: `{"text": "...", "author": "..."}` (author opcional/vazio para frases anônimas).
- 70% inspiracional/clássicas (Cora Coralina, Drummond, Cecília Meireles, Mario Quintana, Paulo Coelho, Clarice Lispector, Aristóteles, Confúcio, Lao-Tsé, Sêneca, Vinicius de Moraes, etc.).
- 30% leve/cotidiano (frases anônimas, motivação suave, bom humor).
- Função `quote_of_the_day(today: date | None = None) -> dict` calcula `today.timetuple().tm_yday % 100` para indexar a lista. Determinístico: mesma frase o dia inteiro, troca à meia-noite (na timezone do servidor Python).

### Frontend

- **Perfil ([pages/3_👤_Perfil.py](pages/3_👤_Perfil.py)):**
  - No formulário, adicionar `st.date_input("Aniversário", value=birthday_atual, min_value=date(1900,1,1), max_value=date.today())`.
  - Streamlit `st.date_input` aceita `value=None` ao passar `value=None`. Para suportar "sem aniversário", oferecemos um `st.checkbox("Tenho aniversário cadastrado")` que mostra/esconde o input, OU simplesmente um `st.date_input` com `value=birthday_atual or date.today()` e considerar `None` se o usuário não mudou. **Decisão:** usar um `st.toggle("Informar aniversário")` simples; se ligado, exibe o `date_input` e envia; se desligado, envia `birthday=None` (limpa).
  - No submit, passa `birthday=date_value.isoformat() if toggle else None` para `update_profile`.

- **Home ([home.py](home.py)):**
  - Carregar `me()` adicionalmente (para pegar `birthday`). Usa o usuário do auth para pegar o `birthday`.
  - **Banner de aniversário:** se `birthday` existe e `(today.month, today.day) == (birthday.month, birthday.day)`, exibir banner com `st.success("🎉 Feliz aniversário, {name}!")` no topo.
  - **Post-it com frase do dia:** sempre exibe (independente de aniversário). Usar `st.info` com formato:
    ```
    💭 *<frase>*
    — <autor>  (se houver)
    ```
  - Ordem na Home: banner aniversário (se houver) → post-it frase do dia → resto (welcome OU dashboard).

### Compatibilidade

- Usuários sem `birthday` (legacy): Perfil mostra toggle desligado; Home não mostra banner.
- Usuários sem nenhuma disciplina: continuam vendo tela de boas-vindas, mas com post-it acima.

### Idioma e segurança

- Documentação/UI em português; nomes técnicos/endpoints em inglês.
- Aniversário é só do próprio usuário (`$auth.id`). Sem leak.

## Risks / Trade-offs

- [Schema migration adiciona campo opcional] → Xano emite "data loss" warning como já estamos acostumadas; seguro confirmar.
- [Frase do dia em fuso do servidor] → Pode parecer "trocar adiantado/atrasado" pra usuários em fusos diferentes. Aceitável; v1 não trata multi-tz.
- [Quote determinístico por dia do ano] → Após 365 dias, repete. Aceitável; quem usa diariamente vai ver repetir só no ano seguinte.
- [Toggle de aniversário no perfil] → UX um pouco mais complexa que um input puro, mas evita o problema "como sinalizar 'sem data' num st.date_input que sempre tem valor". Aceitável.
