// Creates a new academic task for the authenticated user
function "academic_tasks/create_task" {
  input {
    // The title of the task.
    text title
  
    // A description of the task (optional).
    text description?
  
    // The due date of the task (optional).
    date due_date?
  
    // The status of the task: pending / in_progress / done.
    text status
  
    // The priority of the task: low / medium / high (optional).
    text priority?
  
    // The subject the task belongs to (must be owned by the user).
    int subject_id
  }

  stack {
    // Verify that the title is not empty
    precondition ($input.title != null && $input.title != "") {
      error_type = "badrequest"
      error = "Task title cannot be empty."
    }
  
    // Get the subject by ID
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    // Verify that the subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    // Verify that the authenticated user is the owner of the subject
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You are not authorized to create tasks for this subject."
    }
  
    // Add a new task record
    db.add academic_tasks {
      data = {
        created_at : "now"
        updated_at : "now"
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        priority   : $input.priority
        status     : $input.status
        subject_id : $input.subject_id
        user_id    : $auth.id
      }
    } as $new_task
  }

  response = $new_task
  tags = ["edutrack"]
}