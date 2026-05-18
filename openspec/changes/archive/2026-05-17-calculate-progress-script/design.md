## Context

O EduTrack AI tem frontend em Streamlit (Python) e backend em XanoScript. As `academic_tasks` possuem um campo `status` (text). Foi solicitado um script Python utilitário para medir progresso. Entrega limitada à geração do arquivo (AGENTS.md Regra Nº2).

## Goals / Non-Goals

**Goals:**
- Função Python pura que calcula `concluídas / total` e devolve JSON.
- Robusta a entrada vazia (sem divisão por zero) e a erros (`try/except`).

**Non-Goals:**
- Buscar dados no Xano (API/DB) — o script recebe a lista de tarefas como entrada.
- Persistência, interface Streamlit, testes automatizados.
- Qualquer push/sync/deploy.

## Decisions

- **Localização:** `scripts/calculate_progress.py` (diretório `scripts/` novo; fora do XanoScript).
- **Assinatura:** `calculate_progress(tasks: list[dict]) -> str` retornando JSON via `json.dumps`. Cada tarefa é um `dict` com a chave `status`.
  - *Alternativa considerada:* retornar `dict` em vez de string JSON — descartada porque o pedido foi explícito "retorne um JSON".
- **Definição de "concluída":** `status == "done"`, alinhado às funções de `subjects`/`academic_tasks` já existentes no projeto.
- **Saída:** `{"total": int, "completed": int, "percentage": float}` com `percentage` arredondado a 2 casas.
- **Divisão por zero:** se `total == 0`, `percentage = 0.0`.
- **Erros:** bloco `try/except` envolvendo o cálculo, conforme AGENTS.md (Python deve usar try/except em lógica complexa); em erro, retorna JSON com chave `error`.
- **Execução direta:** bloco `if __name__ == "__main__":` com exemplo simples, para uso manual/CLI.
- **Idioma:** documentação/comentários em português; nomes de variáveis/funções em inglês.

## Risks / Trade-offs

- [Formato de entrada não especificado pelo usuário] → Assumida lista de dicts com chave `status`; documentado aqui. Ajustável se a fonte real de dados (API/CSV) for definida depois.
- [Critério "done" fixo] → Alinhado ao restante do projeto; se houver outros estados finais, exigirá ajuste em change futura.
- [Sem testes automatizados] → Fora de escopo (não solicitado); cenários da spec servem como base de verificação manual.
