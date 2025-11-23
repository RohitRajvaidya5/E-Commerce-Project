from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from .models import Product
from django.core.mail import send_mail
from .utils import send_order_email
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings


def test_email(request, to_email, subject, message):
    success = send_order_email(
        to_email=to_email,
        subject=subject,
        message=message
    )

    return HttpResponse("Email sent successfully!" if success else "Failed to send email")


def search_suggestions(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse({"results": []})

    products = Product.objects.filter(name__icontains=query)[:5]

    data = [{"name": p.name, "url": p.get_absolute_url()} for p in products]

    return JsonResponse({"results": data})


def search_products(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return redirect("products")   # or "home"

    results = Product.objects.filter(name__icontains=query)

    return render(request, "products/search_results.html", {
        "query": query,
        "results": results,
    })



def products(request):
    product = Product.objects.all()
    return render(request, "products/index.html", {"products": product})


def home(request):
    profile = Profile.objects.all()
    product = Product.objects.all()
    cart = request.session.get("cart", {})
    cart_items = sum(cart.values())
    return render(request, "base.html", {"cart_items": cart_items, "products": product}, {"profile": profile})

@login_required(login_url='login')
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "products/detail.html", {"product": product})


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart

    if request.method == "POST" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "qty": cart[str(product_id)],
            "message": "Product added to cart"
        })

    return redirect("products")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")


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

    return render(request, "products/cart.html", {"products": products, "total": total})


def update_cart_quantity(request, product_id, quantity):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        quantity = max(1, int(quantity))

        if str(product_id) not in cart:
            return JsonResponse({"success": False, "error": "Product not in cart"}, status=400)

        cart[str(product_id)] = quantity
        request.session["cart"] = cart

        product = Product.objects.get(id=product_id)
        new_total = product.price * quantity

        return JsonResponse({"qty": quantity, "total": new_total, "success": True})

    return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def checkout(request):
    profile = Profile.objects.get(user=request.user)
    cart = request.session.get("cart", {})
    products = []
    subtotal = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * qty
        product.qty = qty
        product.item_total = item_total
        products.append(product)
        subtotal += item_total

    tax = int(subtotal * 0.10)
    total = subtotal + tax

    # ---------- Razorpay Client ----------
    client = razorpay.Client(auth=(
    settings.RAZORPAY_KEY_ID,
    settings.RAZORPAY_KEY_SECRET
))
    razorpay_payment_data = None

    # ---------- Auto-fill user details ----------
    user = request.user
    profile = user.profile

    name = user.username
    email = user.email               # <-- CORRECT: email stored in User model
    phone = profile.phone or ""      # <-- Profile
    address = profile.address or ""

    # ---------- IF user edits form manually ----------
    if request.method == "POST":
        name = request.POST.get("name", name)
        email = request.POST.get("email", email)
        phone = request.POST.get("phone", phone)
        address = request.POST.get("address", address)

    # ---------- Step 1: Create Razorpay Payment ----------

    if request.method == "POST" and "create_payment" in request.POST:
        amount = int(total * 100)

        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1,
        })

        razorpay_payment_data = {
            "key_id": settings.RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "amount": amount,
            "currency": "INR",
        }

    # ---------- Step 2: Verify & Save Order ----------
    if request.method == "POST" and "place_order" in request.POST:
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        params = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }

        # Payment verification
        try:
            client.utility.verify_payment_signature(params)
            payment_status = "Success"
        except:
            payment_status = "Failed"

        # Save order
        order = Order.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            total_price=total,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_order_id=razorpay_order_id,
            razorpay_signature=razorpay_signature,
            payment_status=payment_status
        )

        order.products.set([p.id for p in products])

        # Email confirmation
        send_order_email(
            to_email=email,
            subject="Order Confirmation",
            message=f"Thank you {name}! Your order ID is {order.id}\nPayment Amount : {order.total_price}\nPayment Status: {order.payment_status}"
        )

        # Empty cart
        request.session["cart"] = {}

        return redirect("success")

    return render(request, "products/checkout.html", {
        "products": products,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "payment": razorpay_payment_data,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "profile": profile,
    }, )




def success(request):
    return render(request, "products/success.html")
