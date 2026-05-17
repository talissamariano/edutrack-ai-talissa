// Creates a new subject
query subjects verb=POST {
  api_group = "subjects"
  auth = "user"

  input {
    // The name of the subject.
    text name
  
    // A description of the subject.
    text description
  }

  stack {
    // Run the function to create the subject
    function.run "subjects/create_subject" {
      input = {name: $input.name, description: $input.description}
    } as $new_subject
  }

  response = $new_subject
  tags = ["edutrack"]
}