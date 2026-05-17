// Deletes a subject for the authenticated user
function "subjects/delete_subject" {
  input {
    // The ID of the subject to delete.
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
      error = "You are not authorized to delete this subject."
    }
  
    // Delete the subject record (db.del does not return the deleted record)
    db.del subjects {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = $subject
  tags = ["edutrack"]
}