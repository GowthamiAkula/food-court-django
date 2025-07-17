from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import MenuItem, Feedback, Order, OrderItem

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


# Register View
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'accounts/register.html')


# Home View
@login_required
def home_view(request):
    return render(request, 'accounts/home.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Menu View
def menu_view(request):
    items = MenuItem.objects.all()
    return render(request, 'accounts/menu.html', {'items': items})


# Add to Cart
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1

    request.session['cart'] = cart
    messages.success(request, "Item added to cart!")
    return redirect('menu')


# View Cart
def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for item_id, quantity in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            item_total = menu_item.price * quantity
            items.append({
                'item': menu_item,
                'quantity': quantity,
                'item_total': item_total
            })
            total += item_total
        except MenuItem.DoesNotExist:
            continue

    context = {
        'items': items,
        'total': total
    }
    return render(request, 'accounts/cart.html', context)


# Clear Cart
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')


# Feedback View
def feedback_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        Feedback.objects.create(name=name, email=email, message=message)
        messages.success(request, "Thank you for your feedback! 💖")
        return redirect('feedback')

    return render(request, 'accounts/feedback.html')


# ✅ Place Order View
@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('menu')

    # Create order for logged in user
    order = Order.objects.create(user=request.user)

    # Add each cart item to OrderItem
    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                item_name=item.name,
                quantity=quantity,
                price=item.price
            )
        except MenuItem.DoesNotExist:
            continue

    # Clear cart and show success message
    request.session['cart'] = {}
    messages.success(request, f"🎉 Order placed successfully! Your Order ID is #{order.id}")
    return redirect('menu')


# ✅ View My Orders Page
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/my_orders.html', {'orders': orders})
