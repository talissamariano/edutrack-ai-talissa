## Why

O EduTrack AI armazena obrigações acadêmicas (`academic_tasks`) com um campo `status`, mas não há forma de medir o progresso do aluno (quantas tarefas estão concluídas em relação ao total). Um utilitário simples de cálculo de progresso permite reaproveitar essa lógica em relatórios ou na interface.

## What Changes

- Criar o script Python `scripts/calculate_progress.py`.
- O script calcula a porcentagem de progresso: `concluídas / total`.
- O script retorna um resultado em formato JSON.
- Tratamento de erros com `try/except` (incluindo divisão por zero quando `total = 0`).

Fora de escopo (não solicitado): integração com APIs Xano, persistência, interface Streamlit, testes automatizados.

## Capabilities

### New Capabilities
- `progress-calculation`: Lógica utilitária em Python que calcula a porcentagem de tarefas concluídas em relação ao total e retorna o resultado em JSON.

### Modified Capabilities
<!-- Nenhuma capability existente tem requisitos alterados. -->

## Impact

- **Novo arquivo:** `scripts/calculate_progress.py` (Python, fora do XanoScript).
- **Sem impacto no backend Xano:** nenhuma tabela/API/função XanoScript é criada ou alterada.
- **Sem push/deploy:** entrega limitada à geração do arquivo (AGENTS.md Regra Nº2).
