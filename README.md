# Introduction

<ol>
  <br><li><a href="https://www.djangoproject.com/">Django Web Site</a></li>
  <br><li><a href="https://docs.djangoproject.com/en/4.1/">Django documentation</a></li>
  <br><li><a href="https://www.djangoproject.com/download/">Django Installation</a>
    <ul>
     <br><li>pip install Django</li>
    </ul>
  </li>
  <br><li><a href="https://www.w3schools.com/django/django_create_virtual_environment.php">Create Virtual Environment</a>
    <ul>
     <br><li>In Windows: py -m venv myVenvName</li>
     <br><li>In MacOS: python -m venv myVenvName</li>
     <br><li>In Linux: python3 -m venv myVenvName</li>
    </ul>
  </li>
  <br><li>cd Current venv
    <ul>
     <br><li>In Windows cmd: myVenvName\Scripts\activate.bat</li>
     <br><li>In MacOS: source myVenvName/bin/activate</li>
     <br><li>In Linux: source myVenvName/bin/activate</li>
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
     <br><li>Create Project with additional folder : django-admin startproject myNewProject</li>
     <br><li>Create Project without additional folder : django-admin startproject myNewProject .</li>
    </ul>
  </li>
  <br><li>Learn manage.py step by step
    <ul>
     <br><li>In Windows: py manage.py</li>
     <br><li>In MacOS: python manage.py</li>
     <br><li>In Linux: python3 manage.py</li>
    </ul>
  </li>
  <br><li>Create first app
    <ul>
     <br><li>In Windows: py manage.py startapp myFirstApp</li>
     <br><li>In MacOS: python manage.py startapp myFirstApp</li>
     <br><li>In Linux: python3 manage.py startapp myFirstApp</li>
    </ul>
  </li>
  <br><li>set new app in config\settings.py
    <ul>
     <br><li>insert 'myFristApp'</li>
    </ul>
  </li>
  <br><li>Link myFirstApp in config\urls.py
    <ul>
     <br><li>import include from django.urls</li>
     <br><li>add path('myFirstApp/', include('myFirstApp.urls'))</li>
    </ul>
  </li>
  <br><li>Create urls.py file in myFirstApp
    <ul>
     <br><li>import path from django.urls</li>
     <br><li>import views from .</li>
     <br><li>add urlpatterns list for urls</li>
     <br><li>add path('hello/', views.hello, name='hello')</li>
    </ul>
  </li>
  <br><li>Write hello function for myFirstApp
    <ul>
     <br><li>import HttpResponse from django.http</li>
     <br><li>import views from .</li>
     <br><li>Difine a def for hello with request parameter</li>
     <br><li>Write return HttpResponse('Hello World')</li>
     <br><li>In Windows: py manage.py runserver</li>
     <br><li>In MacOS: python manage.py runserver</li>
     <br><li>In Linux: python3 manage.py runserver</li>
    </ul>
  </li>
</ol>
