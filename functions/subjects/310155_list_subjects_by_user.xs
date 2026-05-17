// Lists all subjects for the authenticated user
function "subjects/list_subjects_by_user" {
  input {
    // If true, also returns archived subjects. Defaults to false.
    bool include_archived?
  }

  stack {
    // Conditionally query subjects based on the include_archived flag
    conditional {
      if ($input.include_archived) {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id
          return = {type: "list"}
        } as $subjects
      }
    
      else {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id && $db.subjects.archived_at == null
          return = {type: "list"}
        } as $subjects
      }
    }
  }

  response = $subjects
  tags = ["edutrack"]
}