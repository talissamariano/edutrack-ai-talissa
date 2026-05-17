// Creates a new subject for the authenticated user
function "subjects/create_subject" {
  input {
    // The name of the subject.
    text name
  
    // A description of the subject.
    text description
  }

  stack {
    // Verify that the name is not empty
    precondition ($input.name != null && $input.name != "") {
      error_type = "badrequest"
      error = "Subject name cannot be empty."
    }
  
    // Add a new subject record
    db.add "" {
      data = {
        created_at : "now"
        updated_at : "now"
        name       : $input.name
        description: $input.description
        user_id    : $auth.id
      }
    } as $new_subject
  }

  response = $new_subject
  tags = ["edutrack"]
}