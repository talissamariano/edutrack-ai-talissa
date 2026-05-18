"""Utilitario para calcular o progresso de obrigacoes academicas.

Calcula a porcentagem de tarefas concluidas em relacao ao total
e retorna o resultado em formato JSON.
"""

import json

# Status que indica uma tarefa concluida (alinhado ao restante do projeto).
COMPLETED_STATUS = "done"


def calculate_progress(tasks):
    """Calcula o progresso das tarefas e retorna uma string JSON.

    Args:
        tasks: lista de dicts, cada um com a chave "status".

    Returns:
        str: JSON com as chaves "total", "completed" e
        "percentage". Em caso de erro, JSON com a chave "error".
    """
    try:
        total = len(tasks)
        completed = sum(1 for task in tasks if task.get("status") == COMPLETED_STATUS)

        # Trata total == 0 para evitar divisao por zero.
        if total == 0:
            percentage = 0.0
        else:
            percentage = round((completed / total) * 100, 2)

        result = {
            "total": total,
            "completed": completed,
            "percentage": percentage,
        }
        return json.dumps(result)
    except Exception as error:  # noqa: BLE001 - retorna erro como JSON
        return json.dumps({"error": str(error)})


if __name__ == "__main__":
    # Exemplo de uso manual.
    example_tasks = [
        {"status": "done"},
        {"status": "pending"},
        {"status": "done"},
        {"status": "pending"},
    ]
    print(calculate_progress(example_tasks))
