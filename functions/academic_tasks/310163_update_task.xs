// Updates an academic task for the authenticated user
function "academic_tasks/update_task" {
  input {
    // The ID of the task to update.
    int id
  
    // The new title (optional).
    text title?
  
    // The new description (optional).
    text description?
  
    // The new due date (optional).
    date due_date?
  
    // The new status (optional).
    text status?
  
    // The new priority: low / medium / high (optional).
    text priority?
  
    // The new subject (optional; must be owned by the user when provided).
    int subject_id?
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
      error = "You are not authorized to update this task."
    }
  
    // If a new subject is provided, verify the user owns it
    conditional {
      if ($input.subject_id != null) {
        db.get subjects {
          field_name = "id"
          field_value = $input.subject_id
        } as $new_subject
      
        precondition ($new_subject != null) {
          error_type = "notfound"
          error = "New subject not found."
        }
      
        precondition ($new_subject.user_id == $auth.id) {
          error_type = "accessdenied"
          error = "You are not authorized to move the task to this subject."
        }
      }
    }
  
    // Update the task record
    db.edit academic_tasks {
      field_name = "id"
      field_value = $input.id
      data = {
        updated_at : "now"
        title      : $input.title
        description: $input.description
        priority   : $input.priority
        due_date   : $input.due_date
        status     : $input.status
        subject_id : $input.subject_id
      }
    } as $updated_task
  }

  response = $updated_task
  tags = ["edutrack"]
}