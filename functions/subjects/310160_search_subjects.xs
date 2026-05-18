// Searches subjects for the authenticated user by name and/or overdue tasks
function "subjects/search_subjects" {
  input {
    text name?
    bool only_overdue?
  }

  stack {
    var $has_name {
      value = $input.name != null && ($input.name|trim) != ""
    }
  
    var $overdue_subject_ids {
      value = []
    }
  
    conditional {
      if ($input.only_overdue) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.status != "done" && $db.academic_tasks.due_date < "now"
          return = {type: "list"}
        } as $overdue_tasks
      
        var.update $overdue_subject_ids {
          value = `($overdue_tasks|map:$$.subject_id)|unique`
        }
      }
    }
  
    conditional {
      if ($has_name && $input.only_overdue) {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id && ($db.subjects.name includes $input.name || $db.subjects.id in $overdue_subject_ids)
          return = {type: "list"}
        } as $subjects
      }
    
      elseif ($has_name) {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id && $db.subjects.name includes $input.name
          return = {type: "list"}
        } as $subjects
      }
    
      elseif ($input.only_overdue) {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id && $db.subjects.id in $overdue_subject_ids
          return = {type: "list"}
        } as $subjects
      }
    
      else {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id
          return = {type: "list"}
        } as $subjects
      }
    }
  }

  response = $subjects
  tags = ["edutrack"]
}