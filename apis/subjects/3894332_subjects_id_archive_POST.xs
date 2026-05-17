// Archives a subject
query "subjects/{id}/archive" verb=POST {
  api_group = "subjects"
  auth = "user"

  input {
    // The ID of the subject to archive.
    int id
  }

  stack {
    // Run the function to archive the subject
    function.run "subjects/archive_subject" {
      input = {id: $input.id}
    } as $archived_subject
  }

  response = $archived_subject
  tags = ["edutrack"]
}