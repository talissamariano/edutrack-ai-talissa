# home-dashboard Specification (delta)

## ADDED Requirements

### Requirement: Banner de aniversário

A Home SHALL exibir um banner de parabéns no topo da página quando o dia e mês atuais coincidem com o `birthday` do usuário autenticado.

#### Scenario: Aniversário hoje

- **WHEN** o usuário autenticado abre a Home num dia em que `(hoje.mês, hoje.dia) == (birthday.mês, birthday.dia)`
- **THEN** a Home exibe um banner de parabéns no topo, antes do dashboard ou da tela de boas-vindas

#### Scenario: Não é aniversário

- **WHEN** hoje não coincide com o aniversário do usuário (ou ele não tem aniversário cadastrado)
- **THEN** nenhum banner de aniversário é exibido

### Requirement: Frase do dia (post-it)

A Home SHALL exibir uma "frase do dia" em formato de post-it (componente nativo Streamlit, sem CSS), sorteada deterministicamente pelo dia do ano a partir de uma lista local em PT-BR com 100 itens. A mesma frase SHALL aparecer ao longo do dia e SHALL trocar à meia-noite.

#### Scenario: Frase persiste durante o dia

- **WHEN** o usuário abre a Home várias vezes no mesmo dia
- **THEN** a mesma frase é exibida em todas as aberturas

#### Scenario: Frase muda no dia seguinte

- **WHEN** o dia muda (passa da meia-noite)
- **THEN** a Home exibe uma frase diferente, escolhida a partir do dia do ano

#### Scenario: Sem dependência externa

- **WHEN** a frase do dia é determinada
- **THEN** a operação NÃO realiza chamadas de rede externas (a lista é local em `lib/quotes.py`)
