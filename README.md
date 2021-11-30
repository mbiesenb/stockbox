# stockbox
Back-End of a social media app

## Setting up the project
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



