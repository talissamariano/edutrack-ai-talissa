// Marks an academic task as done for the authenticated user
function "academic_tasks/complete_task" {
  input {
    // The ID of the task to complete.
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
      error = "You are not authorized to complete this task."
    }
  
    // Set status to done
    db.edit academic_tasks {
      field_name = "id"
      field_value = $input.id
      data = {updated_at: "now", status: "done"}
    } as $updated_task
  }

  response = $updated_task
  tags = ["edutrack"]
}