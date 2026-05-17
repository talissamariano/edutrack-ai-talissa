// Lists all subjects for the authenticated user
query subjects verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
    // If true, also returns archived subjects. Defaults to false.
    bool include_archived?
  }

  stack {
    // Run the function to list the subjects
    function.run "subjects/list_subjects_by_user" {
      input = {include_archived: $input.include_archived}
    } as $subjects
  }

  response = $subjects
  tags = ["edutrack"]
}