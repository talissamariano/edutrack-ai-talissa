// Deletes a subject
query "subjects/{id}" verb=DELETE {
  api_group = "subjects"
  auth = "user"

  input {
    // The ID of the subject to delete.
    int id
  }

  stack {
    // Run the function to delete the subject
    function.run "subjects/delete_subject" {
      input = {id: $input.id}
    } as $deleted_subject
  }

  response = $deleted_subject
  tags = ["edutrack"]
}