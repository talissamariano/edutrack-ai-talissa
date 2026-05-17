// Stores subjects created by users
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    timestamp updated_at?=now
    timestamp archived_at?
    text name filters=trim
    text description
    int user_id {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
  ]

  tags = ["edutrack"]
}