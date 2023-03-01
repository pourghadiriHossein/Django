# Learn How to Use Templates File and Load Variable and Set Condition in Django Template File

## <a href="https://www.w3schools.com/django/django_create_virtual_environment.php">Create Virtual Environment</a>
### In Windows
```bash
py -m venv myVenvName
```
### In MacOS
```bash
python -m venv myVenvName
```
### In Linux
```bash
python3 -m venv myVenvName
```

## cd Current venv
### In Windows cmd
```bash
myVenvName\Scripts\activate.bat
```
### In MacOS
```bash
source myVenvName/bin/activate
```
### In Linux
```bash
source myVenvName/bin/activate
```

## <a href="https://www.w3schools.com/django/django_install_django.php">Install Django</a>
### In Windows
```bash
py -m pip install Django
```
### In MacOS
```bash
python -m pip install Django
```
### In Linux
```bash
python3 -m pip install Django
```

## <a href="https://www.w3schools.com/django/django_create_project.php">Django Create Project</a>
### Create Project without additional folder
```bash
django-admin startproject myNewProject .
```

## Create app webPage
### In Windows
```bash
py manage.py startapp webPage
```
### In MacOS
```bash
python manage.py startapp webPage
```
### In Linux
```bash
python3 manage.py startapp webPage
```

## set new app in config\settings.py - insert 'webPage'

## Link homePage in config\urls.py
```bash
from django.urls import include
```
```bash
add path('webPage/', include('webPage.urls'))
```

## Create templates Folder in webPage App
### Create home.html File
### Create hcj.html File
### Create django.html File
### Create laravel.html File

## Create urls.py file in webPage
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home_page, name='home'),
    path('hcj/', views.show_hcj_page, name='hcj'),
    path('django/', views.show_django_page, name='django'),
    path('laravel/', views.show_laravel_page, name='laravel'),
]
```

## Write hello function for homePage views.py
```bash
from django.shortcuts import render

def {FUNCTION NAME}(request):
    return render(request, '{TEMPLATE-FILE-NAME}.html', context)
```

## Template context Variable
```bash
context = {
  'key': 'value'
}
```

## URL Command In Django Template
```bash
{% url 'Your URL Name' %}
```

## Set Condition and Load Data Commands In Django Template
```bash
% for student in  students%}
  {{ student.id }}
{% endfor %}
```

## Run Your App
### In Windows
```bash
py manage.py runserver
```
### In MacOS
```bash
python manage.py runserver
```
### In Linux
```bash
python3 manage.py runserver
```

## Simple HTML Template For Index
```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{WEB SITE TITLE}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body class="container-xxl">
    <div class="row">
        <aside class="col-sm-3 pt-5 text-center">
            <div class="d-grid gap-1">
                <a href="{YOUR URL}" type="button" class="btn btn-primary btn-block">Home</a>
                <a href="{YOUR URL}" type="button" class="btn btn-primary btn-block">HCJ Class</a>
                <a href="{YOUR URL}" type="button" class="btn btn-primary btn-block">Django Class</a>
                <a href="{YOUR URL}" type="button" class="btn btn-primary btn-block">Laravel Class</a>
            </div>
        </aside>
        <article class="col-sm-9 p-5">
            <h1 class="text-center">Welcome To My Web Site</h1>
            <hr>
            <h2 class="text-center pt-5">Check Your Class From Left Side Bar</h2>
        </article>
    </div>
</body>
</html>
```

## Simple HTML Template For Course
```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{WEB SITE TITLE}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body class="container-xxl">
    <div class="row">
        <aside class="col-sm-3 pt-5 text-center">
            <div class="d-grid gap-1">
                <a href="{YOUR URL}" type="button" class="btn btn-primary btn-block">Home</a>
                <a href="{YOUR URL}" type="button" class="btn btn-primary btn-block">HCJ Class</a>
                <a href="{YOUR URL}" type="button" class="btn btn-primary btn-block">Django Class</a>
                <a href="{YOUR URL}" type="button" class="btn btn-primary btn-block">Laravel Class</a>
            </div>
        </aside>
        <article class="col-sm-9 p-5">
            <h1>HTML, CSS, JavaScript Class</h1>
            <hr>
            <section>
                <table class="table table-striped table-hover table-bordered text-center">
                    <thead class="bg-warning">
                      <tr>
                        <th scope="col">ID</th>
                        <th scope="col">First Name</th>
                        <th scope="col">Last Name</th>
                        <th scope="col">Age</th>
                        <th scope="col">Phone</th>
                      </tr>
                    </thead>
                    <tbody>
                        {START YOUR FOR}
                        <tr>
                          <th scope="row">{{ YOUR DATA }}</th>
                          <td>{{ YOUR DATA }}</td>
                          <td>{{ YOUR DATA }}</td>
                          <td>{{ YOUR DATA }}</td>
                          <td>{{ YOUR DATA }}</td>
                        </tr>
                        {END YOUR FOR}
                    </tbody>
                  </table>
            </section>
        </article>
    </div>
</body>
</html>
```
  
