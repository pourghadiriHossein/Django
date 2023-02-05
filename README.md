# Learn How to Use Templates File and Load Variable and Set Condition in Django Template File

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
  <br><li>Create webPage app
    <ul>
     <br><li>In Windows: py manage.py startapp car</li>
     <br><li>In MacOS: python manage.py startapp car</li>
     <br><li>In Linux: python3 manage.py startapp car</li>
    </ul>
  </li>
  <br><li>set car app in config\settings.py
    <ul>
     <br><li>insert 'webPage'</li>
    </ul>
  </li>
  <br><li>Link car in config\urls.py
    <ul>
     <br><li>import include from django.urls</li>
     <br><li>add path('webPage/', include('webPage.urls'))</li>
    </ul>
  </li>
  <br><li>Create templates Folder in webPage App
    <ul>
     <br><li>Create home.html File</li>
     <br><li>Create hcj.html File</li>
     <br><li>Create django.html File</li>
     <br><li>Create laravel.html File</li>
    </ul>
  </li>
  <br><li>Create urls.py file in webPage
    <ul>
     <br><li>import path from django.urls</li>
     <br><li>import views from .</li>
     <br><li>add urlpatterns list for urls</li>
     <br><li>add path('', views.index, name='index')</li>
     <br><li>add path('bmw/', views.bmw, name='bmw')</li>
     <br><li>add path('benz/', views.benz, name='benz')</li>
     <br><li>add path('dodge/', views.dodge, name='dodge')</li>
    </ul>templates
  </li>
  <br><li>Create urls.py file in football
    <ul>
     <br><li>import path from django.urls</li>
     <br><li>import views from .</li>
     <br><li>add urlpatterns list for urls</li>
     <br><li>add path('', views.show_home_page, name='home')</li>
     <br><li>add path('hcj/', views.show_hcj_page, name='hcj')</li>
     <br><li>add path('django/', views.show_django_page, name='django')</li>
     <br><li>add path('laravel/', views.show_laravel_page, name='laravel')</li>
    </ul>
  </li>
  <br><li>Write Necessary function for webPage App in views.py
    <ul>
     <br><li>import render from django.shortcuts</li>
     <br><li>Difine a def for Necessary function with request parameter</li>
     <br><li>return request with your target HTML file by render function and you can send context file to HTML file</li>
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
  <br><li>Simple HTML Template For Sub Category
    <pre>
    
    </pre>
  </li>
</ol>
