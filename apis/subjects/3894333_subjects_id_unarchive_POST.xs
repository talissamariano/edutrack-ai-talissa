// Unarchives a subject
query "subjects/{id}/unarchive" verb=POST {
  api_group = "subjects"
  auth = "user"

  input {
    // The ID of the subject to unarchive.
    int id
  }

  stack {
    // Run the function to unarchive the subject
    function.run "subjects/unarchive_subject" {
      input = {id: $input.id}
    } as $unarchived_subject
  }

  response = $unarchived_subject
  tags = ["edutrack"]
}