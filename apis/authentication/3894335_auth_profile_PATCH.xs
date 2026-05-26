// Updates the authenticated user's profile (name and/or email)
query "auth/profile" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    // The new name for the authenticated user.
    text name? filters=trim
  
    // The new email for the authenticated user.
    email email? filters=trim|lower
  
    // The user's birthday (optional).
    date birthday?
  }

  stack {
    // Get the authenticated user's current record
    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $user
  
    // Verify that the user exists
    precondition ($user != null) {
      error_type = "notfound"
      error = "User not found."
    }
  
    // If the email is being changed, ensure it is unique
    conditional {
      if ($input.email != null && $input.email != $user.email) {
        db.get user {
          field_name = "email"
          field_value = $input.email
        } as $existing
      
        precondition ($existing == null) {
          error_type = "accessdenied"
          error = "An account with this email already exists."
        }
      }
    }
  
    // Update only the authenticated user's record
    db.edit user {
      field_name = "id"
      field_value = $auth.id
      data = {
        name    : $input.name
        email   : $input.email
        birthday: $input.birthday
      }
    } as $updated_user
  
    // Create an event log for the profile update
    function.run "Quick Start/log_event" {
      input = {
        user_id : $updated_user.id
        action  : "update_profile"
        metadata: $updated_user
      }
    } as $event_log
  }

  response = {
    id        : $updated_user.id
    created_at: $updated_user.created_at
    name      : $updated_user.name
    email     : $updated_user.email
    role      : $updated_user.role
  }

  tags = ["edutrack"]
}