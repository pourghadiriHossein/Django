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
     <br><li>insert 'car'</li>
    </ul>
  </li>
  <br><li>set football app in config\settings.py
    <ul>
     <br><li>insert 'football'</li>
    </ul>
  </li>
  <br><li>set musicBand app in config\settings.py
    <ul>
     <br><li>insert 'musicBand'</li>
    </ul>
  </li>
  <br><li>Link car in config\urls.py
    <ul>
     <br><li>import include from django.urls</li>
     <br><li>add path('car/', include('car.urls'))</li>
    </ul>
  </li>
  <br><li>Link football in config\urls.py
    <ul>
     <br><li>import include from django.urls</li>
     <br><li>add path('football/', include('football.urls'))</li>
    </ul>
  </li>
  <br><li>Link musicBand in config\urls.py
    <ul>
     <br><li>import include from django.urls</li>
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
  <br><li>Simple HTML Template
    <pre>
    &lt;!DOCTYPE html&gt;
    &lt;html lang="en"&gt;
    &lt;head&gt;
      &lt;meta charset="UTF-8"&gt;
      &lt;meta http-equiv="X-UA-Compatible" content="IE=edge"&gt;
      &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
      &lt;title&gt;Document&lt;/title&gt;
      &lt;style&gt;
          *{
              font-size: 100px;
          }
      &lt;/style&gt;
    &lt;/head&gt;
    &lt;body&gt;
      &lt;label for="likes" id="likes"&gt;0&lt;/label&gt;
      &lt;input type="button" value="👍" onclick="increse_likes()"&gt;
      &lt;br&gt;
      &lt;label for="" id="galb"&gt;❤️&lt;/label&gt;
      &lt;script&gt;
          function sleep(ms) {
              return new Promise(resolve => setTimeout(resolve, ms));
          }
          async function increse_likes(){
              var likes = document.getElementById("likes");
              n = parseInt(likes.innerHTML);
              console.log(n);
              likes.innerHTML = n+1;
              var size = document.getElementById('galb');
              for(var i=100; i<120; i++){
                  size.style.fontSize = i+'px';
                  await sleep (1)
              }
              for(var i=120; i>99; i--){
                  size.style.fontSize = i+'px';
                  await sleep (1)
              }
          }
      &lt;/script&gt;
    &lt;/body&gt;
    &lt;/html&gt;
    </pre>
  </li>
</ol>
