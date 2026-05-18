// Updates a subject
query "subjects/{id}" verb=PATCH {
  api_group = "subjects"
  auth = "user"

  input {
    // The ID of the subject to update.
    int id
  
    // The new name of the subject.
    text name
  
    // The new description of the subject.
    text description
  }

  stack {
    // Run the function to update the subject
    function.run "subjects/update_subject" {
      input = {
        id         : $input.id
        name       : $input.name
        description: $input.description
      }
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["edutrack"]
}