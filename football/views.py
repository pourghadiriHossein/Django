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
            <title>Football</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://digwallpapers.com/wallpapers/full/c/4/2/38950-2560x1600-soccer-background-desktop-hd.jpg);
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
                <p class="guide">Use This List Football In Route</p>
                <ul class="list">
                  <li class="item">ronaldo</li>
                  <li class="item">messi</li>
                  <li class="item">karim</li>
                </ul>
            </div>
        </body>
    </html>
    ''')


def ronaldo(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ronaldo</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://wallpapercave.com/wp/wp2565631.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')

def messi(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Messi</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://cdn.wallpapersafari.com/77/59/s71ixH.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')

def karim(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Karim</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://w0.peakpx.com/wallpaper/198/351/HD-wallpaper-karim-benzema-real-madrid-french-footballer-portrait-gray-stone-background-football-la-liga.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')
