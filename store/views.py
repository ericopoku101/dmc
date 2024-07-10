from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from . utils import cookieCart, cartData
# Create your views here.


def store(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    

    products = Product.objects.all()
    context = {
        'products':products,
        'cartItems':cartItems
        }
    return render(request, 'store/store.html', context)

def main(request):
    context = {}

    return render(request, 'store/main.html', context)

def checkout(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

    
def cart(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
            
    context = {'items': items, 'order':order, 'cartItem':cartItems}

    return render(request, 'store/cart.html', context)

def updateItem(request):
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId) 

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('item was added', safe= False)

        
        
    
    