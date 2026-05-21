// Updates a subject for the authenticated user
function "subjects/update_subject" {
  input {
    // The ID of the subject to update.
    int id
  
    // The new name of the subject.
    text name
  
    // The new description of the subject (optional).
    text description?
  
    // The new professor of the subject.
    text professor
  
    // New workload in hours (optional).
    int workload_hours?
  
    // New course semester / period (optional).
    int semester?
  }

  stack {
    // Get the subject by ID
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $subject
  
    // Verify that the subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    // Verify that the authenticated user is the owner of the subject
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You are not authorized to update this subject."
    }
  
    // Verify that the name is not empty
    precondition ($input.name != null && $input.name != "") {
      error_type = "badrequest"
      error = "Subject name cannot be empty."
    }
  
    // Update the subject record
    db.edit subjects {
      field_name = "id"
      field_value = $input.id
      data = {
        updated_at    : "now"
        name          : $input.name
        description   : $input.description
        professor     : $input.professor
        workload_hours: $input.workload_hours
        semester      : $input.semester
      }
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["edutrack"]
}