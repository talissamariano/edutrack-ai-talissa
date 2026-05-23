// Shortcut: marks an academic task as done
query "academic_tasks/{id}/complete" verb=POST {
  api_group = "academic_tasks"
  auth = "user"

  input {
    // The ID of the task to complete.
    int id
  }

  stack {
    // Run the function to complete the task
    function.run "academic_tasks/complete_task" {
      input = {id: $input.id}
    } as $completed_task
  }

  response = $completed_task
  tags = ["edutrack"]
}