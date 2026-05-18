// Stores academic tasks created by users, linked to subjects
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    timestamp updated_at?=now
    timestamp archived_at?
    text title filters=trim
    text description
    date due_date
    text status
    int subject_id {
      table = "subjects"
    }
  
    int user_id {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
  ]

  tags = ["edutrack"]
}