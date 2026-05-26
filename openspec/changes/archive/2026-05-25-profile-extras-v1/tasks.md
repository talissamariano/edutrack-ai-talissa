## 1. Schema e backend Xano

- [x] 1.1 Adicionar `date birthday?` ao schema da tabela `user` em `tables/837130_user.xs`
- [x] 1.2 Atualizar `apis/authentication/3894321_auth_me_GET.xs` para incluir `"birthday"` na lista `output` do `db.get user`
- [x] 1.3 Atualizar `apis/authentication/3894335_auth_profile_PATCH.xs` para declarar `date birthday?` no input e incluir `birthday: $input.birthday` no `data` do `db.edit user`

## 2. Helper Streamlit

- [x] 2.1 Estender `update_profile` em `lib/xano_client.py` para aceitar `birthday: str | None = None` (omitido do payload quando None)

## 3. Lista de frases (lib/quotes.py)

- [x] 3.1 Criar `lib/quotes.py` com lista `QUOTES` de 100 itens (cada item dict com `text` e `author` opcional) — 70% inspiracional/clássicas + 30% leve/cotidiano
- [x] 3.2 Implementar `quote_of_the_day(today: date | None = None) -> dict` usando `today.timetuple().tm_yday % len(QUOTES)`

## 4. Perfil — campo de aniversário

- [x] 4.1 Em `pages/3_👤_Perfil.py`, exibir o aniversário atual no resumo de "Dados atuais" (formato DD/MM/YYYY) quando houver
- [x] 4.2 No formulário "Editar perfil", adicionar `st.toggle("Informar aniversário")` que controla a visibilidade de um `st.date_input("Aniversário")`
- [x] 4.3 No submit, enviar `birthday=date_value.isoformat() if toggle else ""` para `update_profile`

## 5. Home — banner de aniversário + frase do dia

- [x] 5.1 Carregar `me()` adicionalmente em `home.py` para obter o `birthday` (e exibir nome no banner)
- [x] 5.2 Se hoje (mês+dia) == aniversário do usuário, exibir banner com `st.success("🎉 Feliz aniversário, <nome>!")` no topo
- [x] 5.3 Exibir post-it com a `quote_of_the_day()` usando `st.info` com texto + autor — sempre, abaixo do banner (se houver) e antes do dashboard / welcome

## 6. Qualidade

- [x] 6.1 Sanidade Python (`ast.parse`) em `lib/quotes.py`, `lib/xano_client.py`, `home.py`, `pages/3_👤_Perfil.py`
- [x] 6.2 Verificar ausência de `unsafe_allow_html=True` para estilo
