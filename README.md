# how to Load Image, CSS, Java Script File in Django Template

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
  <br><li>Create homePage app
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
     <br><li>add path('home-page/', include('homePage.urls'))</li>
    </ul>
  </li>
  <br><li>Create templates Folder in homePage App
    <ul>
      <br><li>Create index.html File</li>
    </ul>
  </li>
  <br><li>Create static Folder in homePage App
    <ul>
      <br><li>Create css Folder
        <ol>
          <br><li>style.css</li>
        </ol>
      </li>
      <br><li>Create js Folder
        <ol>
          <br><li>main.js</li>
        </ol>
      </li>
      <br><li>Create image Folder
        <ol>
          <br><li>Add logo.png File</li>
          <br><li>Add 4 Image File For Slide Show</li>
        </ol>
      </li>
    </ul>
  </li>
  <br><li>Create urls.py file in homePage App
    <ul>
     <br><li>import path from django.urls</li>
     <br><li>import views from .</li>
     <br><li>add urlpatterns list for urls</li>
     <br><li>add path('', views.index)</li>
    </ul>
  </li>
  <br><li>Write Necessary function for homePage App in views.py
    <ul>
     <br><li>import render from django.shortcuts</li>
     <br><li>Difine a def for Necessary function with request parameter</li>
     <br><li>return request with your target HTML file by render function</li>
     <br><li>Without context: return render(request, '{Your Target HTML File}')</li>
     <br><li>With context: return render(request, '{Your Target HTML File}', context)</li>
     <br><li>
      Template context Variable<br>
      <pre>
      context = {
        'key': 'value'
      }
      </pre>
      </li>
     <br><li>In Windows: py manage.py runserver</li>
     <br><li>In MacOS: python manage.py runserver</li>
     <br><li>In Linux: python3 manage.py runserver</li>
    </ul>
  </li>
  <br><li>Simple HTML Template For Index
    <pre>
    &lt;!DOCTYPE html&gt;
    &lt;html lang="en"&gt;
    &lt;head&gt;
        &lt;meta charset="UTF-8"&gt;
        &lt;meta http-equiv="X-UA-Compatible" content="IE=edge"&gt;
        &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
        &lt;title&gt;Home Page&lt;/title&gt;
        &lt;link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"&gt;
        &lt;script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"&gt;&lt;/script&gt;
    &lt;/head&gt;
    &lt;body&gt;
        &lt;nav class="navbar navbar-expand-sm bg-dark navbar-dark" id="nav"&gt;
            &lt;div class="container-fluid"&gt;
                &lt;a class="navbar-brand" href="javascript:void(0)"&gt;
                    &lt;img src="{% static 'image/logo.png' %}" alt="logo" width="40px"&gt;
                &lt;/a&gt;
                &lt;button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar"&gt;
                &lt;span class="navbar-toggler-icon"&gt;&lt;/span&gt;
                &lt;/button&gt;
                &lt;div class="collapse navbar-collapse" id="collapsibleNavbar"&gt;
                &lt;ul class="navbar-nav"&gt;
                    &lt;li class="nav-item"&gt;
                    &lt;a class="nav-link text-light" href="javascript:void(0)" onclick="red()"&gt;Red&lt;/a&gt;
                    &lt;/li&gt;
                    &lt;li class="nav-item"&gt;
                    &lt;a class="nav-link text-light" href="javascript:void(0)" onclick="blue()"&gt;Blue&lt;/a&gt;
                    &lt;/li&gt;
                    &lt;li class="nav-item"&gt;
                    &lt;a class="nav-link text-light" href="javascript:void(0)" onclick="yellow()"&gt;Yellow&lt;/a&gt;
                    &lt;/li&gt;
                    &lt;li class="nav-item"&gt;
                        &lt;a class="nav-link text-light" href="javascript:void(0)" onclick="cyan()"&gt;Cyan&lt;/a&gt;
                    &lt;/li&gt; 
                    &lt;li class="nav-item"&gt;
                        &lt;a class="nav-link text-light" href="javascript:void(0)" onclick="gray()"&gt;Gray&lt;/a&gt;
                    &lt;/li&gt;    
                &lt;/ul&gt;
                &lt;/div&gt;
            &lt;/div&gt;
        &lt;/nav&gt;
        &lt;div id="demo" class="carousel slide" data-bs-ride="carousel"&gt;
            &lt;!-- Indicators/dots --&gt;
            &lt;div class="carousel-indicators"&gt;
              &lt;button type="button" data-bs-target="#demo" data-bs-slide-to="0" class="active"&gt;&lt;/button&gt;
              &lt;button type="button" data-bs-target="#demo" data-bs-slide-to="1"&gt;&lt;/button&gt;
              &lt;button type="button" data-bs-target="#demo" data-bs-slide-to="2"&gt;&lt;/button&gt;
              &lt;button type="button" data-bs-target="#demo" data-bs-slide-to="3"&gt;&lt;/button&gt;
            &lt;/div&gt;
            &lt;!-- The slideshow/carousel --&gt;
            &lt;div class="carousel-inner"&gt;
              &lt;div class="carousel-item active"&gt;
                &lt;img src="{% static 'image/image1.avif' %}" alt="image1" class="d-block" style="width:100%; height: 93vh;"&gt;
              &lt;/div&gt;
              &lt;div class="carousel-item"&gt;
                &lt;img src="{% static 'image/image2.jpg' %}" alt="image2" class="d-block" style="width:100%; height: 93vh;"&gt;
              &lt;/div&gt;
              &lt;div class="carousel-item"&gt;
                &lt;img src="{% static 'image/image3.jpg' %}" alt="image3" class="d-block" style="width:100%; height: 93vh;"&gt;
              &lt;/div&gt;
              &lt;div class="carousel-item"&gt;
                &lt;img src="{% static 'image/image4.jpg' %}" alt="image4" class="d-block" style="width:100%; height: 93vh;"&gt;
              &lt;/div&gt;
            &lt;/div&gt;
            &lt;!-- Left and right controls/icons --&gt;
            &lt;button class="carousel-control-prev" type="button" data-bs-target="#demo" data-bs-slide="prev"&gt;
              &lt;span class="carousel-control-prev-icon">&lt;/span&gt;
            &lt;/button&gt;
            &lt;button class="carousel-control-next" type="button" data-bs-target="#demo" data-bs-slide="next"&gt;
              &lt;span class="carousel-control-next-icon"&gt;&lt;/span&gt;
            &lt;/button&gt;
        &lt;/div&gt;
    &lt;/body&gt;
    &lt;/html&gt;
    </pre>
  </li>
  <br><li>URL Command In Django Template
    <pre>
      {% url 'Your URL Name' %}
    </pre>
  </li>
  <br><li>Set Condition and Load Data Commands In Django Template
    <pre>
      {% for student in  students%}
        {{ student.id }}
      {% endfor %}
    </pre>
  </li>
</ol>
