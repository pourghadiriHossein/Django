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
  <br><li>Create car app
    <ul>
     <br><li>In Windows: py manage.py startapp car</li>
     <br><li>In MacOS: python manage.py startapp car</li>
     <br><li>In Linux: python3 manage.py startapp car</li>
    </ul>
  </li>
  <br><li>Create football app
    <ul>
     <br><li>In Windows: py manage.py startapp football</li>
     <br><li>In MacOS: python manage.py startapp football</li>
     <br><li>In Linux: python3 manage.py startapp football</li>
    </ul>
  </li>
  <br><li>Create musicBand app
    <ul>
     <br><li>In Windows: py manage.py startapp musicBand</li>
     <br><li>In MacOS: python manage.py startapp musicBand</li>
     <br><li>In Linux: python3 manage.py startapp musicBand</li>
    </ul>
  </li>
  <br><li>set car app in config\settings.py
    <ul>
     <br><li>insert 'car', 'football', 'musicBand'</li>
    </ul>
  </li>
  <br><li>Link car in config\urls.py
    <ul>
     <br><li>import include from django.urls</li>
     <br><li>add path('car/', include('car.urls'))</li>
     <br><li>add path('football/', include('football.urls'))</li>
     <br><li>add path('musicBand/', include('musicBand.urls'))</li>
    </ul>
  </li>
  <br><li>Create urls.py file in car
    <ul>
     <br><li>import path from django.urls</li>
     <br><li>import views from .</li>
     <br><li>add urlpatterns list for urls</li>
     <br><li>add path('', views.index, name='index')</li>
     <br><li>add path('bmw/', views.bmw, name='bmw')</li>
     <br><li>add path('benz/', views.benz, name='benz')</li>
     <br><li>add path('dodge/', views.dodge, name='dodge')</li>
    </ul>
  </li>
  <br><li>Create urls.py file in football
    <ul>
     <br><li>import path from django.urls</li>
     <br><li>import views from .</li>
     <br><li>add urlpatterns list for urls</li>
     <br><li>add path('', views.index, name='index')</li>
     <br><li>add path('ronaldo/', views.ronaldo, name='ronaldo')</li>
     <br><li>add path('messi/', views.messi, name='messi')</li>
     <br><li>add path('karim/', views.karim, name='karim')</li>
    </ul>
  </li>
  <br><li>Create urls.py file in musicBand
    <ul>
     <br><li>import path from django.urls</li>
     <br><li>import views from .</li>
     <br><li>add urlpatterns list for urls</li>
     <br><li>add path('', views.index, name='index')</li>
     <br><li>add path('BTS/', views.BTS, name='BTS')</li>
     <br><li>add path('Queen/', views.Queen, name='Queen')</li>
     <br><li>add path('Pink-Floyd/', views.Pink_Floyd, name='Pink_Floyd')</li>
    </ul>
  </li>
  <br><li>Write Necessary function for car, football, musicBand in views.py
    <ul>
     <br><li>import render from django.shortcuts</li>
     <br><li>import HttpResponse from django.http</li>
     <br><li>Difine a def for Necessary function with request parameter</li>
     <br><li>Write return HttpResponse(''' {YOUR HTML FILE} ''')</li>
     <br><li>In Windows: py manage.py runserver</li>
     <br><li>In MacOS: python manage.py runserver</li>
     <br><li>In Linux: python3 manage.py runserver</li>
    </ul>
  </li>
  <br><li>Simple HTML Template
    <pre>
    &lt;!DOCTYPE html&gt;
    &lt;html lang="en"&gt;
        &lt;head&gt;
            &lt;meta charset="UTF-8"&gt;
            &lt;meta http-equiv="X-UA-Compatible" content="IE=edge"&gt;
            &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
            &lt;title&gt;Car&lt;/title&gt;
            &lt;style&gt;
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://coolthemestores.com/wp-content/uploads/2021/10/neon-cars-wallpaper-background.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
                .list-background {
                  width: 40%;
                  margin: 2% auto;
                  min-height: 400px;
                  background-color: rgba(240, 240, 240, 0.5);
                  padding: 2%;
                  text-align: center;
                }
                .guide {
                  font-size: xx-large;
                  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
                  font-weight: bold;
                  margin: 3% 0;
                }
                .list {
                  list-style: none;
                }
                .item {
                  font-size: 26px;
                  font-weight: bold;
                  font-style: italic;
                  font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
                  letter-spacing: 2px;
                  margin: 5% auto;
                  background-image: linear-gradient(to left, rgb(189, 51, 189), rgb(103, 207, 207));
                  width: 40%;
                  padding: 3%;
                  border-radius: 4px;
                  color: white;
                }
            &lt;/style&gt;
        &lt;/head&gt;
        &lt;body&gt;
            &lt;div class="list-background"&gt;
                &lt;p class="guide"&gt;Use This List Car In Route&lt;/p&gt;
                &lt;ul class="list"&gt;
                  &lt;li class="item"&gt;bmw&lt;/li&gt;
                  &lt;li class="item"&gt;benz&lt;/li&gt;
                  &lt;li class="item"&gt;doge&lt;/li&gt;
                &lt;/ul&gt;
            &lt;/div&gt;
        &lt;/body&gt;
    &lt;/html&gt;
    </pre>
  </li>
</ol>
