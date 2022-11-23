from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Cart
from django.conf import settings
from django.http.response import JsonResponse
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


def index(request):
    template = loader.get_template('app/index.html')
    items = Item.objects.all().values()
    cart = Cart.objects.all().values()
    context = {
        'items': items,
        'carts': cart,
        'stripe_pass_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return HttpResponse(template.render(context))


def cart(request):
    template = loader.get_template('app/cart.html')
    cart = Cart.objects.all().values()
    context = {
        'carts': cart,
    }
    return HttpResponse(template.render(context))


def add(request):
    template = loader.get_template('app/addProduct.html')
    cart = Cart.objects.all().values()
    context = {
        'carts': cart
    }
    return HttpResponse(template.render(context))


@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        count = request.POST['count']
        item = Item(name=name, description=description,
                    price=price, count=count)
        item.save()
        return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def checkout(request):
    cart = Cart.objects.all().values()
    domain = "http://127.0.0.1:8000"
    items = []
    for i in cart:
        items.append(
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(i['price']) * 100,
                    'product_data': {
                                'name': i['name'],
                    }
                },
                'quantity': i['quantity'],
            },
        )
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=domain + '/success/',
            cancel_url=domain + '/',
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
        )
        return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def add_to_cart(request, id):
    item = Item.objects.get(id=id)
    cart = Cart.objects.filter(item_id=id).values()
    if cart:
        item.count -= 1
        item.save(update_fields=['count'])
        cart.update(quantity=cart[0]['quantity']+1)
    else:
        item.count = item.count-1
        item.save(update_fields=['count'])
        cart = Cart(name=item.name, description=item.description,
                    price=item.price, item_id=id, quantity=1)
        cart.save()

    return redirect('index')


def minus_cart(request, id):
    cart = Cart.objects.get(id=id)
    item = Item.objects.get(id=cart.item_id)
    if cart.quantity == 1:
        cart.delete()
        item.count += 1
        item.save(update_fields=['count'])
        return HttpResponseRedirect(reverse('cart'))
    elif cart.quantity > 0:
        cart.quantity -= 1
        item.count += 1
        item.save(update_fields=['count'])
        cart.save(update_fields=['quantity'])
        return HttpResponseRedirect(reverse('cart'))
    else:
        return HttpResponseRedirect(reverse('cart'))


def plus_cart(request, id):
    cart = Cart.objects.get(id=id)
    item = Item.objects.get(id=cart.item_id)
    if item.count > 0:
        cart.quantity += 1
        item.count -= 1
        item.save(update_fields=['count'])
        cart.save(update_fields=['quantity'])
        return HttpResponseRedirect(reverse('cart'))
    else:
        return HttpResponseRedirect(reverse('cart'))


def remove_cart(request, id):
    cart = Cart.objects.get(id=id)
    item = Item.objects.get(id=cart.item_id)
    item.count += cart.quantity
    item.save(update_fields=['count'])
    cart.delete()
    return redirect('cart')


def checkout_success(request):
    Cart.objects.all().delete()
    template = loader.get_template('app/success.html')
    return HttpResponse(template.render())
