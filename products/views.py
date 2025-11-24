from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

import razorpay

from accounts.models import Profile
from orders.models import Order
from .models import Product
from .utils import send_order_email


def run_migrations(request):
    secret = request.GET.get("secret")

    if secret != settings.MIGRATION_SECRET:
        return HttpResponse("Unauthorized", status=401)

    call_command("migrate")
    return HttpResponse("Migrations applied successfully")


def test_email(request, to_email, subject, message):
    success = send_order_email(
        to_email=to_email,
        subject=subject,
        message=message,
    )

    if success:
        msg = "Email sent successfully!"
    else:
        msg = "Failed to send email"

    return HttpResponse(msg)


def search_suggestions(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse({"results": []})

    products = Product.objects.filter(name__icontains=query)[:5]

    data = [
        {"name": p.name, "url": p.get_absolute_url()}
        for p in products
    ]

    return JsonResponse({"results": data})


def search_products(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return redirect("products")

    results = Product.objects.filter(name__icontains=query)

    return render(
        request,
        "products/search_results.html",
        {"query": query, "results": results},
    )


def products(request):
    product_list = Product.objects.all()

    return render(
        request,
        "products/index.html",
        {"products": product_list},
    )


def home(request):
    product_list = Product.objects.all()
    profile_list = Profile.objects.all()
    cart = request.session.get("cart", {})
    cart_items = sum(cart.values())

    return render(
        request,
        "base.html",
        {
            "cart_items": cart_items,
            "products": product_list,
            "profile": profile_list,
        },
    )


@login_required(login_url="login")
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    return render(
        request,
        "products/detail.html",
        {"product": product},
    )


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart

    is_ajax = (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
    )

    if request.method == "POST" or is_ajax:
        return JsonResponse(
            {
                "success": True,
                "qty": cart[str(product_id)],
                "message": "Product added to cart",
            }
        )

    return redirect("products")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart

    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        product.qty = qty
        product.total = product.price * qty
        items.append(product)
        total += product.total

    return render(
        request,
        "products/cart.html",
        {"products": items, "total": total},
    )


def update_cart_quantity(request, product_id, quantity):
    if request.method == "POST":
        cart = request.session.get("cart", {})

        try:
            qty_int = int(quantity)
        except ValueError:
            return JsonResponse(
                {"success": False, "error": "Invalid quantity"},
                status=400,
            )

        qty_int = max(1, qty_int)

        if str(product_id) not in cart:
            return JsonResponse(
                {"success": False, "error": "Product not in cart"},
                status=400,
            )

        cart[str(product_id)] = qty_int
        request.session["cart"] = cart

        product = Product.objects.get(id=product_id)
        new_total = product.price * qty_int

        return JsonResponse(
            {"qty": qty_int, "total": new_total, "success": True}
        )

    return JsonResponse(
        {"success": False, "error": "Invalid method"},
        status=405,
    )


@login_required(login_url="login")
def checkout(request):
    profile = Profile.objects.get(user=request.user)
    cart = request.session.get("cart", {})
    items = []
    subtotal = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        product.qty = qty
        product.item_total = product.price * qty
        items.append(product)
        subtotal += product.item_total

    tax = int(subtotal * 0.10)
    total = subtotal + tax

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    razorpay_data = None

    user = request.user
    profile = user.profile

    name = user.username
    email = user.email
    phone = profile.phone or ""
    address = profile.address or ""

    if request.method == "POST":
        name = request.POST.get("name", name)
        email = request.POST.get("email", email)
        phone = request.POST.get("phone", phone)
        address = request.POST.get("address", address)

    if request.method == "POST" and "create_payment" in request.POST:
        amount = int(total * 100)

        order = client.order.create(
            {
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1,
            }
        )

        razorpay_data = {
            "key_id": settings.RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "amount": amount,
            "currency": "INR",
        }

    if request.method == "POST" and "place_order" in request.POST:
        rp_id = request.POST.get("razorpay_payment_id")
        rp_order = request.POST.get("razorpay_order_id")
        rp_sig = request.POST.get("razorpay_signature")

        params = {
            "razorpay_order_id": rp_order,
            "razorpay_payment_id": rp_id,
            "razorpay_signature": rp_sig,
        }

        try:
            client.utility.verify_payment_signature(params)
            pay_status = "Success"
        except Exception:
            pay_status = "Failed"

        order = Order.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            total_price=total,
            razorpay_payment_id=rp_id,
            razorpay_order_id=rp_order,
            razorpay_signature=rp_sig,
            payment_status=pay_status,
        )

        order.products.set([p.id for p in items])

        message = (
            f"Thank you {name}! Your order ID is {order.id}\n"
            f"Payment Amount: {order.total_price}\n"
            f"Payment Status: {order.payment_status}"
        )

        send_order_email(
            to_email=email,
            subject="Order Confirmation",
            message=message,
        )

        request.session["cart"] = {}

        return redirect("success")

    return render(
        request,
        "products/checkout.html",
        {
            "products": items,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "payment": razorpay_data,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "profile": profile,
        },
    )


def success(request):
    return render(request, "products/success.html")
