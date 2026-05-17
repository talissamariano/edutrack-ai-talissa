// Archives a subject for the authenticated user
function "subjects/archive_subject" {
  input {
    // The ID of the subject to archive.
    int id
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
      error = "You are not authorized to archive this subject."
    }
  
    // Verify that the subject is not already archived
    precondition ($subject.archived_at == null) {
      error_type = "badrequest"
      error = "Subject is already archived."
    }
  
    // Update the subject record to set the archived_at timestamp
    db.edit subjects {
      field_name = "id"
      field_value = $input.id
      data = {archived_at: "now"}
    } as $archived_subject
  }

  response = $archived_subject
  tags = ["edutrack"]
}