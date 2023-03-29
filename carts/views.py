from django.shortcuts import redirect, render
from carts.models import Cart, CartItem
from store.models import Product

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id = product_id) #getting the product
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) #getting the cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
    cart_item.save()
    return redirect('cart')
    

def remove_cart(request, product_id):
    product = Product.objects.get(id = product_id) #getting the product
    cart = Cart.objects.get(cart_id = _cart_id(request)) #getting the cart
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    product = Product.objects.get(id = product_id) #getting the product
    cart = Cart.objects.get(cart_id = _cart_id(request)) #getting the cart
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()

    return redirect('cart')


def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total+=cart_item.product.price*cart_item.quantity
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total+tax
    except Exception:
        pass
    context = {'total': total, 'quantity' : quantity, 'cart_items':cart_items, 'tax':tax, 'grand_total':grand_total}
    return render(request, 'store/cart.html', context)