// Searches subjects for the authenticated user by name and/or overdue tasks
query "subjects/search" verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
    // Optional text to match against the subject name.
    text name?
  
    // If true, only returns subjects that have overdue tasks.
    bool only_overdue?
  }

  stack {
    // Run the function to search the subjects
    function.run "subjects/search_subjects" {
      input = {name: $input.name, only_overdue: $input.only_overdue}
    } as $subjects
  }

  response = $subjects
  tags = ["edutrack"]
}