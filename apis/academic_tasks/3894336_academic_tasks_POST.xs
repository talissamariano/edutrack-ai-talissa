// Creates a new academic task
query academic_tasks verb=POST {
  api_group = "academic_tasks"
  auth = "user"

  input {
    // The title of the task.
    text title
  
    // The subject the task belongs to (must be owned by the user).
    int subject_id
  
    // A description of the task (optional).
    text description?
  
    // The due date of the task (optional).
    date due_date?
  
    // The status: pending / in_progress / done.
    text status
  }

  stack {
    // Run the function to create the task
    function.run "academic_tasks/create_task" {
      input = {
        title      : $input.title
        subject_id : $input.subject_id
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
      }
    } as $new_task
  }

  response = $new_task
  tags = ["edutrack"]
}