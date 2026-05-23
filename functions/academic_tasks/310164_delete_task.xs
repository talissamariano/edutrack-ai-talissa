// Deletes an academic task for the authenticated user
function "academic_tasks/delete_task" {
  input {
    // The ID of the task to delete.
    int id
  }

  stack {
    // Get the task by ID
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $task
  
    // Verify that the task exists
    precondition ($task != null) {
      error_type = "notfound"
      error = "Task not found."
    }
  
    // Verify ownership of the task
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You are not authorized to delete this task."
    }
  
    // Delete the task record (db.del does not return the deleted record)
    db.del academic_tasks {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = $task
  tags = ["edutrack"]
}