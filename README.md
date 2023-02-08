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
        &lt;title&gt;WebPage Home&lt;/title&gt;
        &lt;link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"&gt;
        &lt;script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"&gt;&lt;/script&gt;
    &lt;/head&gt;
    &lt;body class="container-xxl"&gt;
        &lt;div class="row"&gt;
            &lt;aside class="col-sm-3 pt-5 text-center"&gt;
                &lt;div class="d-grid gap-1"&gt;
                    &lt;a href="Your Route Name" type="button" class="btn btn-primary btn-block"&gt;Home&lt;/a&gt;
                    &lt;a href="Your Route Name" type="button" class="btn btn-primary btn-block"&gt;HCJ Class&lt;/a&gt;
                    &lt;a href="Your Route Name" type="button" class="btn btn-primary btn-block"&gt;Django Class&lt;/a&gt;
                    &lt;a href="Your Route Name" type="button" class="btn btn-primary btn-block"&gt;Laravel Class&lt;/a&gt;
                &lt;/div&gt;
            &lt;/aside&gt;
            &lt;article class="col-sm-9 p-5"&gt;
                &lt;h1 class="text-center"&gt;Welcome To My Web Site&lt;/h1&gt;
                &lt;hr&gt;
                &lt;h2 class="text-center pt-5"&gt;Check Your Class From Left Side Bar&lt;/h2&gt;
            &lt;/article&gt;
        &lt;/div&gt;
    &lt;/body&gt;
    &lt;/html&gt;
    </pre>
  </li>
  <br><li>Simple HTML Template For Sub Category
    <pre>
    &lt;!DOCTYPE html&gt;
    &lt;html lang="en"&gt;
    &lt;head&gt;
        &lt;meta charset="UTF-8"&gt;
        &lt;meta http-equiv="X-UA-Compatible" content="IE=edge"&gt;
        &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
        &lt;title&gt;WebPage Home&lt;/title&gt;
        &lt;link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"&gt;
        &lt;script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"&gt;&lt;/script&gt;
    &lt;/head&gt;
    &lt;body class="container-xxl"&gt;
        &lt;div class="row"&gt;
            &lt;aside class="col-sm-3 pt-5 text-center"&gt;
                &lt;div class="d-grid gap-1"&gt;
                    &lt;a href="Your Route Name" type="button" class="btn btn-primary btn-block"&gt;Home&lt;/a&gt;
                    &lt;a href="Your Route Name" type="button" class="btn btn-primary btn-block"&gt;HCJ Class&lt;/a&gt;
                    &lt;a href="Your Route Name" type="button" class="btn btn-primary btn-block"&gt;Django Class&lt;/a&gt;
                    &lt;a href="Your Route Name" type="button" class="btn btn-primary btn-block"&gt;Laravel Class&lt;/a&gt;
                &lt;/div&gt;
            &lt;/aside&gt;
            &lt;article class="col-sm-9 p-5"&gt;
                &lt;h1 class="text-center"&gt;HTML, CSS, JavaScript Class&lt;/h1&gt;
                &lt;hr&gt;
                &lt;section&gt;
                    &lt;table class="table table-striped table-hover table-bordered text-center"&gt;
                        &lt;thead class="bg-warning"&gt;
                          &lt;tr&gt;
                            &lt;th scope="col"&gt;ID&lt;/th&gt;
                            &lt;th scope="col"&gt;First Name&lt;/th&gt;
                            &lt;th scope="col"&gt;Last Name&lt;/th&gt;
                            &lt;th scope="col"&gt;Age&lt;/th&gt;
                            &lt;th scope="col"&gt;Phone&lt;/th&gt;
                          &lt;/tr&gt;
                        &lt;/thead&gt;
                        &lt;tbody&gt;
                            &lt;tr&gt;
                              &lt;th scope="row"&gt;Your Student ID&lt;/th&gt;
                              &lt;td&gt;Your Student First Name&lt;/td&gt;
                              &lt;td&gt;Your Student Last Name&lt;/td&gt;
                              &lt;td&gt;Your Student Age&lt;/td&gt;
                              &lt;td&gt;Your Student Phone&lt;/td&gt;
                            &lt;/tr&gt;
                        &lt;/tbody&gt;
                      &lt;/table&gt;
                &lt;/section&gt;
            &lt;/article&gt;
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
