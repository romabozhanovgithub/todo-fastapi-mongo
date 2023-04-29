# todo-fastapi-mongo

## Set Up
### Set up environment
```pip install pipenv```

```pipenv shell```

```pipenv install```
### Prepare env
- Create directory __system_configs__ and file __.env__ in it
- Fill __.env__ file with:
  ```
  DB_HOST=mongodb://
  DB_PORT=27017
  DB_NAME=tasks
  DB_USER=root
  DB_PASSWORD=password
  JWT_SECRET_KEY=secret
  ALGORITHM=HS256
  SECRET_KEY=secret
  GOOGLE_CLIENT_ID= # your google client id
  GOOGLE_CLIENT_SECRET= # your google client secret
  ```
## How to run project
  - `make run` to run project
  - `make linters` to run linters
  - `make test` to run tests
  - `make deploy` to run linters with tests
  
## Google OAuth
  - To auth via google go to `http://127.0.0.1:5000/` and click __Log In__
  - After authentication you will get `access_token`, copy it
  - Go to `http://localhost:5000/docs` and click __Authorize__ button
  - Put in __username__ field your `access_token` (it is done this way to simplify testing)
  
## Project
  - You can find all endpoints by following this <a href="http://localhost:5000/docs">link</a>
  - You can sign up via __email__ and __password__ or via __Google__
  - You can login via __email__ and __password__ or via __Google__
  - You can __Create__, __Retrieve single task__, __Retrieve list of tasks__, __Update task__ and __Delete task__
  - All tasks related to users
  - Project repo has CI/CD pipelines
  
 ## Project structure
 ```
  app/
    core/
      __init__.py
      dependencies.py
      exceptions.py
      settings.py
      utils.py
    db/
      __init__.py
      client.py
      database.py
      utils.py
    routers/
      __init__.py
      auth.py
      task.py
    schemas/
      __init__.py
      auth.py
      helpers.py
      task.py
      user.py
    services/
      __init__.py
      auth.py
      base.py
      mongo.py
      task.py
      user.py
    __init__.py
    main.py
```
