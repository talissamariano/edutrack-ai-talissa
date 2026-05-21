// Creates a new subject for the authenticated user
function "subjects/create_subject" {
  input {
    // The name of the subject.
    text name
  
    // A description of the subject (optional).
    text description?
  
    // The professor of the subject.
    text professor
  
    // Workload in hours (optional).
    int workload_hours?
  
    // Course semester / period (optional).
    int semester?
  }

  stack {
    // Verify that the name is not empty
    precondition ($input.name != null && $input.name != "") {
      error_type = "badrequest"
      error = "Subject name cannot be empty."
    }
  
    // Prevent duplicate (same user, same name and same professor)
    db.query subjects {
      where = $db.subjects.user_id == $auth.id && $db.subjects.name == $input.name && $db.subjects.professor == $input.professor
      return = {type: "single"}
    } as $existing
  
    precondition ($existing == null) {
      error_type = "accessdenied"
      error = "Disciplina ja cadastrada com esse nome e professor."
    }
  
    // Add a new subject record
    db.add subjects {
      data = {
        created_at    : "now"
        updated_at    : "now"
        name          : $input.name
        description   : $input.description
        professor     : $input.professor
        workload_hours: $input.workload_hours
        semester      : $input.semester
        user_id       : $auth.id
      }
    } as $new_subject
  }

  response = $new_subject
  tags = ["edutrack"]
}