// Lists academic tasks for the authenticated user, with optional filters
query academic_tasks verb=GET {
  api_group = "academic_tasks"
  auth = "user"

  input {
    // Filter by subject (optional).
    int subject_id?
  
    // Filter by status: pending / in_progress / done (optional).
    text status?
  
    // If true, return only tasks not done and with due_date in the past.
    bool only_overdue?
  
    // Filter by priority: low / medium / high (optional).
    text priority?
  }

  stack {
    // Run the function to list the tasks
    function.run "academic_tasks/list_tasks" {
      input = {
        subject_id  : $input.subject_id
        status      : $input.status
        only_overdue: $input.only_overdue
        priority    : $input.priority
      }
    } as $tasks
  }

  response = $tasks
  tags = ["edutrack"]
}