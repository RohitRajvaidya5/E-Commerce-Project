
def cart_item_count(request):
    cart = request.session.get("cart", {})
    return {"cart_items": sum(cart.values())}
