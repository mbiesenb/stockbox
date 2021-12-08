# stockbox
A generic back-end of a social media app


* [Setting up project](#setting-up-project)
* [Testing Application](#testing-application)
* [Starting app manually](#starting-app-manually)
* [Adding aditional services](#adding-additional-services)
* [API Documentation](#api-documentation)

## Setting up project
Clone Repository from GitHub
```cmd
git clone https://github.com/mbiesenb/stockbox.git
```
Setting up virtual python environment 
```cmd
python  -m venv env
```
Allow PowerShell Execution (Windows only)
```powershell
Set-ExecutionPolicy RemoteSigned
```
```cmd
.\env\Scripts\Activate.ps1
```

Install libraries
```cmd
pip install django
pip install djangorestframework
pip install djangorestframework_simplejwt
pip install django-binary-database-files
pip install colorama
```

# Testing Application
This custom command will resets the database, makes all migrations an polulates it with static data
```cmd
python .\manage.py populate_db
```

# Starting the app manually
```cmd
python .\manage.py makemigrations
python .\manage.py migrate
python .\manage.py runserver
```

# Adding an aditional service
```cmd
python .\manage.py startapp <Additional Service>
```

# API Documentation
|PATH|METHOD|Description|
| ----------------------------------|--------|--------------|
| /auth/token                       | POST   | Generate an new API token|
| /auth/token/refresh             | POST   | Refresh an existing API token|
| /auth/token/verifys                | POST   | Verify an existing API token  |
| /auth/register                   | POST   | Create an new user |
| /user/{username}              | GET    | Display user profiles + posts |
| /post/{pk}                    | GET    | Display specific post    |
| /post/{pk}/comments            | GET    | Display comments of a post   |
| /core/chats                      | GET    | Display chats for session user   |
| /core/chats/{chat_id}/messages | GET    | Display messages of a specific chat |


