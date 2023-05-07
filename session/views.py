from django.shortcuts import redirect
from shop.models import Discounts

def add_to_session(request, pk):
    flag_for_Loop = True
    quantity = 1
    if request.method == 'POST':
        if request.POST['quantity']:
            quantity = int(request.POST['quantity'])
    if 'cart' in request.session:
        if len(request.session['cart']) > 0:
            for item in request.session['cart']:
                if item[0] == pk: 
                    request.session['cart'][request.session['cart'].index(item)][1] += quantity
                    flag_for_Loop = False
                    break
            if flag_for_Loop:
                request.session['cart'].append([pk, quantity])
        else:
            request.session['cart'].append([pk, quantity])
    else:
        request.session['cart'] = [[pk, quantity]]

    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))

def mines_from_session(request, pk):
    if 'cart' in request.session:
        for item in request.session['cart']:
            if item[0] == pk:
                if request.session['cart'][request.session['cart'].index(item)][1] > 1:
                    request.session['cart'][request.session['cart'].index(item)][1] -= 1
                else:
                    del request.session['cart'][request.session['cart'].index(item)]

    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))

def plus_from_session(request, pk):
    if 'cart' in request.session:
        for item in request.session['cart']:
            if item[0] == pk:
                request.session['cart'][request.session['cart'].index(item)][1] += 1  

    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))
  
def delete_item_from_session(request, pk):
    if 'cart' in request.session:
        for item in request.session['cart']:
            if item[0] == pk:
                del request.session['cart'][request.session['cart'].index(item)]

    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))

def add_discount(request):
    if request.method == 'POST':
        if request.POST['giftCode']:
            gift_code = request.POST['giftCode']
            discount = Discounts.objects.filter(gift_code=gift_code).first()
            if discount:
                if discount.price:
                    if 'discount' in request.session:
                        if len(request.session['discount']) > 0:
                            request.session['discount'].append([int(discount.price)])
                        else:
                            request.session['discount'] = [[int(discount.price)]]
                    else:
                        request.session['discount'] = [[int(discount.price)]]
                    
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))