from django.shortcuts import render

def show_home_page(request):
    return render(request, 'home.html')

def show_hcj_page(request):
    context = {
        'students': [
            {'id':1, 'first_name':'Ali', 'last_name':'Sattari', 'age':15, 'phone':'09336547812'},
            {'id':2, 'first_name':'Meysam', 'last_name':'Esmaielie', 'age':14, 'phone':'09115487936'},
            {'id':3, 'first_name':'Ahmad', 'last_name':'Mehrbun', 'age':15, 'phone':'09301237485'},
            {'id':4, 'first_name':'Soheil', 'last_name':'Mojdehi', 'age':13, 'phone':'09398524613'},
            {'id':5, 'first_name':'Vahid', 'last_name':'Yari', 'age':16, 'phone':'09017291376'},
        ]
    }
    return render(request, 'hcj.html', context)

def show_django_page(request):
    context = {
        'students': [
            {'id':1, 'first_name':'Changiz', 'last_name':'Ghodratian', 'age':15, 'phone':'09334587812'},
            {'id':2, 'first_name':'Sattar', 'last_name':'Lamie', 'age':14, 'phone':'09115241936'},
            {'id':3, 'first_name':'Ario', 'last_name':'Biname', 'age':15, 'phone':'09301235485'},
            {'id':4, 'first_name':'Roham', 'last_name':'Meshkini', 'age':13, 'phone':'09398545813'},
            {'id':5, 'first_name':'Yavar', 'last_name':'Teymori', 'age':16, 'phone':'09017297776'},
        ]
    }
    return render(request, 'django.html', context)

def show_laravel_page(request):
    context = {
        'students': [
            {'id':1, 'first_name':'Rira', 'last_name':'Iemani', 'age':15, 'phone':'09336515412'},
            {'id':2, 'first_name':'Sima', 'last_name':'Montazeri', 'age':14, 'phone':'09115478536'},
            {'id':3, 'first_name':'Sana', 'last_name':'Bastami', 'age':15, 'phone':'09309247485'},
            {'id':4, 'first_name':'Roxana', 'last_name':'Yazani', 'age':13, 'phone':'09398521253'},
            {'id':5, 'first_name':'Elsa', 'last_name':'Rohi', 'age':16, 'phone':'09017298541'},
        ]
    }
    return render(request, 'laravel.html', context)        