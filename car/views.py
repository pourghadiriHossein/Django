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
            <title>Car</title>
            <style>
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
            </style>
        </head>
        <body>
            <div class="list-background">
                <p class="guide">Use This List Car In Route</p>
                <ul class="list">
                  <li class="item">bmw</li>
                  <li class="item">benz</li>
                  <li class="item">doge</li>
                </ul>
            </div>
        </body>
    </html>
    ''')

def bmw(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>BMW</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://www.bmw-motorsport.com/content/dam/bmw/marketBMWSPORTS/bmw-motorsport_com/assets/fascination/wallpaper/bmw-motorsport-m6-gt3-m4-gt4-m240i-customer-racing-wallpaper.jpg.asset.1581519349390.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')

def benz(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Benz</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://wallpaper.dog/large/20547035.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')    

def dodge(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dodge</title>
            <style>
                * {
                  outline: 0;
                  margin: 0;
                  border: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                body {
                  background-image: url(https://wallpaperaccess.com/full/3807790.jpg);
                  background-size: cover;
                  background-repeat: no-repeat;
                }
            </style>
        </head>
        <body>
            
        </body>
    </html>
    ''')
