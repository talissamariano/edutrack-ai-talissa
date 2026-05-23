// Unarchives a subject for the authenticated user
function "subjects/unarchive_subject" {
  input {
    // The ID of the subject to unarchive.
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
      error = "You are not authorized to unarchive this subject."
    }
  
    // Verify that the subject is archived
    precondition ($subject.archived_at != null) {
      error_type = "badrequest"
      error = "Subject is not archived."
    }
  
    // Update the subject record to clear archived_at
    db.edit subjects {
      field_name = "id"
      field_value = $input.id
      data = {archived_at: null}
    } as $unarchived_subject
  }

  response = $unarchived_subject
  tags = ["edutrack"]
}