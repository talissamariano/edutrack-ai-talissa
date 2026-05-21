// Updates a subject
query "subjects/{id}" verb=PATCH {
  api_group = "subjects"
  auth = "user"

  input {
    // The ID of the subject to update.
    int id
  
    // The new name of the subject.
    text name
  
    // The new professor of the subject.
    text professor
  
    // The new description of the subject (optional).
    text description?
  
    // New workload in hours (optional).
    int workload_hours?
  
    // New course semester / period (optional).
    int semester?
  }

  stack {
    // Run the function to update the subject
    function.run "subjects/update_subject" {
      input = {
        id            : $input.id
        name          : $input.name
        professor     : $input.professor
        description   : $input.description
        workload_hours: $input.workload_hours
        semester      : $input.semester
      }
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["edutrack"]
}