from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Music Band</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://w0.peakpx.com/wallpaper/411/68/HD-wallpaper-music-texture-grunge-music-background-music-concepts-background-with-notes-musical-notes.jpg);
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
            </style>
        </head>
        <body>
            <div class="list-background">
                <p class="guide">Use This List Music Band In Route</p>
                <ul class="list">
                  <li class="item">BTS</li>
                  <li class="item">Queen</li>
                  <li class="item">Pink-Floyd</li>
                </ul>
            </div>
        </body>
    </html>
    ''')


def BTS(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>BTS</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://wallpapercave.com/wp/wp9082415.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')


def Queen(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Queen</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://cdn.britannica.com/83/149183-050-25913164/Queen.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')

def Pink_Floyd(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pink-Floyd</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://wallpapercave.com/wp/wp10391192.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')
