// Deletes an academic task
query "academic_tasks/{id}" verb=DELETE {
  api_group = "academic_tasks"
  auth = "user"

  input {
    // The ID of the task to delete.
    int id
  }

  stack {
    // Run the function to delete the task
    function.run "academic_tasks/delete_task" {
      input = {id: $input.id}
    } as $deleted_task
  }

  response = $deleted_task
  tags = ["edutrack"]
}