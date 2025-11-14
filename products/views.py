from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from .models import Product
from django.shortcuts import render


def products(request):
    product = Product.objects.all()
    # return HttpResponse("Welcome to the home page.")
    return render(request, 'products/index.html', {'products': product})

def home(request):
    cart = request.session.get("cart", {})
    cart_items = sum(cart.values())  # total quantity of items in cart
    print(cart_items)  
    return render(request, 'base.html', {'cart_items': cart_items})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})



def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    return redirect("products")

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session["cart"] = cart
    return redirect("cart")

cart_items = 0

def cart_view(request):
    cart = request.session.get("cart", {})
    products = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        product.total = product.price * qty
        product.qty = qty
        products.append(product)
        total += product.total
        cart_items = total

    context = {
        "products": products,
        "total": total
    }
    return render(request, "products/cart.html", context)



def checkout(request):
    cart = request.session.get("cart", {})
    
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        products = []
        total = 0

        for product_id, qty in cart.items():
            product = Product.objects.get(id=product_id)
            total += product.price * qty
            products.append(product)

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total_price=total
        )
        order.products.set(products)

        request.session["cart"] = {}

        return redirect("/success/")

    return render(request, "products/checkout.html")



