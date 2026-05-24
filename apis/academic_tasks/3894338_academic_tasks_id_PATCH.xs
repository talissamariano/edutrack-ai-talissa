// Updates an academic task
query "academic_tasks/{id}" verb=PATCH {
  api_group = "academic_tasks"
  auth = "user"

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
    // Run the function to update the task
    function.run "academic_tasks/update_task" {
      input = {
        id         : $input.id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
        priority   : $input.priority
        subject_id : $input.subject_id
      }
    } as $updated_task
  }

  response = $updated_task
  tags = ["edutrack"]
}