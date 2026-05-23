// Lists academic tasks for the authenticated user, with optional filters
function "academic_tasks/list_tasks" {
  input {
    // Filter by subject (optional).
    int subject_id?
  
    // Filter by status: pending / in_progress / done (optional).
    text status?
  
    // If true, return only tasks not done and with due_date < now.
    bool only_overdue?
  }

  stack {
    var $has_subject {
      value = $input.subject_id != null
    }
  
    var $has_status {
      value = $input.status != null && $input.status != ""
    }
  
    var $only_overdue {
      value = $input.only_overdue == true
    }
  
    conditional {
      if ($has_subject && $has_status && $only_overdue) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.subject_id == $input.subject_id && $db.academic_tasks.status == $input.status && $db.academic_tasks.status != "done" && $db.academic_tasks.due_date < "now"
          return = {type: "list"}
        } as $tasks
      }
    
      elseif ($has_subject && $has_status) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.subject_id == $input.subject_id && $db.academic_tasks.status == $input.status
          return = {type: "list"}
        } as $tasks
      }
    
      elseif ($has_subject && $only_overdue) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.subject_id == $input.subject_id && $db.academic_tasks.status != "done" && $db.academic_tasks.due_date < "now"
          return = {type: "list"}
        } as $tasks
      }
    
      elseif ($has_status && $only_overdue) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.status == $input.status && $db.academic_tasks.status != "done" && $db.academic_tasks.due_date < "now"
          return = {type: "list"}
        } as $tasks
      }
    
      elseif ($has_subject) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.subject_id == $input.subject_id
          return = {type: "list"}
        } as $tasks
      }
    
      elseif ($has_status) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.status == $input.status
          return = {type: "list"}
        } as $tasks
      }
    
      elseif ($only_overdue) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.status != "done" && $db.academic_tasks.due_date < "now"
          return = {type: "list"}
        } as $tasks
      }
    
      else {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id
          return = {type: "list"}
        } as $tasks
      }
    }
  }

  response = $tasks
  tags = ["edutrack"]
}