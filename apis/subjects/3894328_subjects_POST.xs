// Creates a new subject
query subjects verb=POST {
  api_group = "subjects"
  auth = "user"

  input {
    // The name of the subject.
    text name
  
    // The professor of the subject.
    text professor
  
    // A description of the subject (optional).
    text description?
  
    // Workload in hours (optional).
    int workload_hours?
  
    // Course semester / period (optional).
    int semester?
  }

  stack {
    // Run the function to create the subject
    function.run "subjects/create_subject" {
      input = {
        name          : $input.name
        professor     : $input.professor
        description   : $input.description
        workload_hours: $input.workload_hours
        semester      : $input.semester
      }
    } as $new_subject
  }

  response = $new_subject
  tags = ["edutrack"]
}