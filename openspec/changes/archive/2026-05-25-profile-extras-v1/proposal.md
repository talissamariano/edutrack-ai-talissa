# Change: profile-extras-v1

## Why

Pequenos diferenciais para deixar o app mais pessoal: o aluno pode registrar sua data de aniversário e receber uma mensagem de parabéns na Home no dia, e ver uma "frase do dia" como motivação diária. Nada estrutural — é firula que dá alma ao produto.

## What Changes

Escopo restrito à Change A da Onda 2 das melhorias do professor (aniversário + frase do dia). Cada item entrega valor mesmo se feito isolado.

### A — Campo aniversário no perfil
- Schema: novo campo `date birthday?` (opcional) na tabela `user`.
- Backend: `PATCH /auth/profile` aceita `birthday`; `GET /auth/me` retorna `birthday` no output.
- Helper: `update_profile()` aceita `birthday`; `me()` recebe naturalmente.
- Frontend: [pages/3_👤_Perfil.py](pages/3_👤_Perfil.py) ganha campo `st.date_input` para o aniversário.

### B — Mensagem de aniversário na Home
- Quando `hoje (mês + dia)` igual ao `birthday (mês + dia)` do usuário autenticado, a Home exibe um banner de parabéns no topo (antes do dashboard / boas-vindas).

### C — Post-it com frase do dia na Home
- Novo arquivo `lib/quotes.py` com lista hardcoded de **100 frases PT-BR** (70% inspiracional/clássicas com autores; 30% leve/cotidiano).
- Função `quote_of_the_day(today=None)` retorna o item `dia_do_ano % 100` da lista → mesma frase o dia inteiro, troca à meia-noite.
- Home exibe a frase em um post-it (`st.info` ou container) abaixo do banner de aniversário (se houver) e acima do dashboard.

Fora de escopo: gestão de semestre / auto-arquivar (Change B `semester-management`, planejada em separado), tema visual (Onda visual), exportação/relatórios (Módulo E), notificações por e-mail.

## Capabilities

### New Capabilities
<!-- Nenhuma capability nova; expande as existentes. -->

### Modified Capabilities
- `auth-module`: perfil ganha o campo opcional `birthday`.
- `home-dashboard`: ganha duas decorações — banner de aniversário (quando aplicável) e post-it com frase do dia (sempre).

## Impact

- **Schema Xano:** [tables/837130_user.xs](tables/837130_user.xs) ganha `date birthday?`.
- **Backend Xano:**
  - [apis/authentication/3894321_auth_me_GET.xs](apis/authentication/3894321_auth_me_GET.xs) — incluir `birthday` no output.
  - [apis/authentication/3894335_auth_profile_PATCH.xs](apis/authentication/3894335_auth_profile_PATCH.xs) — declarar e gravar `birthday`.
- **Helper:** [lib/xano_client.py](lib/xano_client.py) — `update_profile(birthday=...)`.
- **Frontend:**
  - [pages/3_👤_Perfil.py](pages/3_👤_Perfil.py) — campo de aniversário no formulário.
  - [home.py](home.py) — banner de aniversário + post-it com frase do dia.
- **Novo arquivo:** [lib/quotes.py](lib/quotes.py) com 100 frases + `quote_of_the_day()`.
- **Sem push/deploy** (AGENTS.md Regra Nº2). Push manual no Xano: 3 `.xs`.
