# Introduction

<ol>
  <br><li><a href="https://www.w3schools.com/django/django_create_virtual_environment.php">Create Virtual Environment</a>
    <ul>
     <br><li>In Windows: py -m venv venv</li>
     <br><li>In MacOS: python -m venv venv</li>
     <br><li>In Linux: python3 -m venv venv</li>
    </ul>
  </li>
  <br><li>cd Current venv
    <ul>
     <br><li>In Windows cmd: venv\Scripts\activate.bat</li>
     <br><li>In MacOS: source venv/bin/activate</li>
     <br><li>In Linux: source venv/bin/activate</li>
    </ul>
  </li>
  <br><li><a href="https://www.w3schools.com/django/django_install_django.php">Install Django</a>
    <ul>
     <br><li>In Windows: py -m pip install Django</li>
     <br><li>In MacOS: python -m pip install Django</li>
     <br><li>In Linux: python3 -m pip install Django</li>
    </ul>
  </li>
  <br><li><a href="https://www.w3schools.com/django/django_create_project.php">Django Create Project</a>
    <ul>
     <br><li>Create Project without additional folder : django-admin startproject config .</li>
    </ul>
  </li>
  <br><li>Create home app
    <ul>
     <br><li>In Windows: py manage.py startapp homePage</li>
     <br><li>In MacOS: python manage.py startapp homePage</li>
     <br><li>In Linux: python3 manage.py startapp homePage</li>
    </ul>
  </li>
  <br><li>set homePage app in config\settings.py
    <ul>
     <br><li>insert 'homePage'</li>
    </ul>
  </li>
  <br><li>Link homePage in config\urls.py
    <ul>
     <br><li>import include from django.urls</li>
     <br><li>add path('homePage/', include('homePage.urls'))</li>
    </ul>
  </li>
  <br><li>Create urls.py file in homePage
    <ul>
     <br><li>import path from django.urls</li>
     <br><li>import views from .</li>
     <br><li>add urlpatterns list for urls</li>
     <br><li>add path('home', views.home, name='home')</li>
    </ul>
  </li>
  <br><li>Write home function for homePage in views.py
    <ul>
     <br><li>import HttpResponse from django.http</li>
     <br><li>import views from .</li>
     <br><li>Difine a def for home with request parameter</li>
     <br><li>Write return HttpResponse(''' {YOUR HTML FILE} ''')</li>
     <br><li>In Windows: py manage.py runserver</li>
     <br><li>In MacOS: python manage.py runserver</li>
     <br><li>In Linux: python3 manage.py runserver</li>
    </ul>
  </li>
</ol>
