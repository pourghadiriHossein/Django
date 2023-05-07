from shop import models

def get_cart_session(request):
    cart = request.session.get('cart', None)
    ids_list = []
    if not cart == None:
        for item in cart:
            ids_list.append(item[0])
    selected_product_in_cart = models.Products.objects.filter(id__in=ids_list)
    final_cart_lists = []
    total_price = 0
    for selected_item in selected_product_in_cart:
        for item in cart:
            if selected_item.id == item[0]:
                final_cart_lists.append({'cart_product':selected_item, 'quantity':item[1]})
                if selected_item.discount_id:
                    if selected_item.discount_id.price:
                        price = selected_item.price - selected_item.discount_id.price
                        total_price += price * item[1]
                    elif selected_item.discount_id.percent:
                        computed_price = selected_item.price * selected_item.discount_id.percent/100
                        price = selected_item.price - computed_price
                        total_price += price * item[1]
                else:
                    total_price += selected_item.price * item[1]
                    
    return  final_cart_lists, total_price

def get_discount_session(request):
    total_discount = 0
    discount = request.session.get('discount', None)
    if discount:
        for item in discount:
            total_discount += item[0]
    return total_discount

def clear_session(request, session_name):
    request.session[session_name].clear()
    request.session.modified = True