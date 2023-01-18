from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <style>
            *{
                font-size: 100px;
            }
        </style>
    </head>
    <body>
        <label for="likes" id="likes">0</label>
        <input type="button" value="👍" onclick="increse_likes()">
        <br>
        <label for="" id="galb">❤️</label>
        <script>
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
        </script>
    </body>
    </html>
     ''')
