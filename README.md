# ClassAdmin
[work in progress]

Server side stuff of student/fee management system developed for cram schools/private tuition classes.

## Description

This is a simple CRUD system developed using python flask and mongodb. It exposes REST APIs via flask which are secured with HTTP Token bearer authentication system. As of now, the user can read/update/create/delete student records and also records of fee installments of them.

## How to run

* Open the `config/config.py` and `config/mongo_config.py` and change the settings according to your environment/requirement.

* Run the script `add_sample_data.py` (coming soon!) to add sample user and records into the database.
```
python add_sample_data.py
```

* Run the script classadmin.py. This will start flask's built in server and start listening on localhost:5000
```
python classadmin.py
```

* First you will need to obtain authentication token from the login API before you are able to hit any other APIs.
```
curl -u sample_user:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 -i -X POST "http://127.0.0.1:5000/classadmin/api/login"
```

* Here, sample_user is a, well, sample user present in the users collection which is followed by an SHA256 hash of his password. If authentication was successful, it will print out a token in the body of the response which you can then use to hit the other APIs (You can adjust how long this token will be valid by changing the token validity setting in `config/config.py`.

* Now you can hit the APIs with this token.
```
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1iIsImV4cCI6MTQ4OTg2MDYyMCwiaWF0IjoxNDg5ODU3MDIwfQ.eyJ1c2VybmFtZSI6InZpbmNoYXNrYXIifQ.Tjg7jJhIZzza8zDryhN4tkxbhN1FyUTGPK_rwpXGLnA" -i "http://127.0.0.1:5000/classadmin/api/students"
```


### REST API Documentation

Coming soon!


### Requirements

* mongodb (version 3.2.1)
* python (version 2.7.12)
* flask framework (version 0.11.1)
* flask plugin - flask_httpauth (version 3.2.2)
* flask pymongo plugin
* all of above with their dependencies, ofcourse.


