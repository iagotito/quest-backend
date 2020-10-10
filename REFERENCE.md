# API Reference
  
The documentation of the system endpoints.
  
## Create User
  
__Description__: Creates a new user in the system.
  
__Endpoint__: `[POST] /users`
  
__Required JSON__:
  
| Field | Type | Description |
|:------|:-----|:-------------|
| email | string | User's email |
| name | string | User's name |
| password | string | User's password |
  
__Return__: The endpoint must return a _json_ object with the
status of the user's creation.
  
- `OK` response:  
-- condition: the email does not already exists  
-- status code: `201 CREATED`  
-- _json_ object:
  
```json
{
    "status_code":  "201 CREATED",
    "message":  "User created with success.",
    "data": {
        "email":  "user_email",
        "name":  "user_name",
        "password":  "password"
    }
}
```
  
- `Error` response:  
-- condition: the email already exists  
-- status code: `400 BAD REQUEST`  
-- _json_ object:
  
```json
{
    "status_code":  "400 BAD REQUEST",
    "message":  "Email already registered."
}
```
