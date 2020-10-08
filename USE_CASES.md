# Use cases
  
This file describes what the program should do. If you want to 
contribute but don't know how, these are good things to do.

## 1. Create users

It must be possible to registrate new users to the system.

__Required fields__:

| Field | Description |
| ----- | ------ |
| email |  it's unique and identifies an user |
| name | the user's name |
| password | the password used by user to log in the system

__Endpoint__: `[POST] /users`

 __Description__: Once provided the required fields through an 
 _application/json_ request, the system checks if the user can 
 be created. The user can be created if there is no other user 
 registered with the mentioned email. If the user can be created, 
 it's information are saved in the Users table of the database.

__Return__: The endpoint must return a _json_ object with the 
status of the user's creation. 

* `OK` response:  
    * status code: `201 CREATED`  
    * _json_ object:

```json
{
  "status_code":  "201 CREATED",
  "message":  "User created with sucess.",
  "data": {
    "email":  "user_email",
    "name":  "user_name",
    "password":  "password"
  }
}
```

* `Error` response:  
    * status code: `400 BAD REQUEST`  
    * _json_ object:

```json
{
  "status_code":  "400 BAD REQUEST",
  "message":  "Email already registered."
}
```


