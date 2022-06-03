from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import PizzaModel, CustomerModel, OrderModel


# Pranav
def admin_login_view(request):
    return render(request, "pizzaapp/adminlogin.html")


def authenticate_admin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user and user.username == 'admin':
        login(request, user)
        return redirect('adminhomepage')

    else:
        messages.add_message(request, messages.ERROR, "Invalid Credentials")
        return redirect('adminloginpage')


def signup_user(request):
    username = request.POST['username']
    password = request.POST['password']
    phoneno = request.POST['phoneno']

    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, "User Already Exits...")
        return redirect('homepage')

    User.objects.create_user(username=username, password=password).save()
    lastobject = len(User.objects.all()) - 1
    CustomerModel(userid=User.objects.all()[lastobject].id, phoneno=phoneno).save()
    messages.add_message(request, messages.ERROR, "User Successfully Created...")
    return redirect('homepage')


def user_authenticate(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return redirect('customerpage')

    else:
        messages.add_message(request, messages.ERROR, "Invalid Credentials")
        return redirect('userloginpage')


def homepage_view(request):
    return render(request, 'pizzaapp/homepage.html')


def user_login_view(request):
    return render(request, "pizzaapp/userlogin.html")


# Shrey
def admin_homepage_view(request):
    if not request.user.is_authenticated:
        return redirect('adminloginpage')
    context = {'pizzas': PizzaModel.objects.all()}
    return render(request, 'pizzaapp/adminhomepage.html', context)


def add_pizza(request):
    name = request.POST['pizza']
    price = request.POST['price']
    PizzaModel(name=name, price=price).save()
    return redirect('adminhomepage')


def delete_pizza(request, pizzapk):
    PizzaModel.objects.filter(id=pizzapk).delete()
    return redirect('adminhomepage')


def log_out_admin(request):
    logout(request)
    return redirect('adminloginpage')


def admin_orders(request):
    orders = OrderModel.objects.all()
    context = {'orders': orders}
    return render(request, 'pizzaapp/admin_orders.html', context)


def accept_order(request, orderpk):
    order = OrderModel.objects.filter(id=orderpk)[0]
    order.status = "Accepted"
    order.save()
    return redirect(request.META['HTTP_REFERER'])


def decline_order(request, orderpk):
    order = OrderModel.objects.filter(id=orderpk)[0]
    order.status = "Declined"
    order.save()
    return redirect(request.META['HTTP_REFERER'])


#   SAMIR
def customer_welcome_view(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    username = request.user.username
    context = {'username': username, 'pizzas': PizzaModel.objects.all()}
    return render(request, 'pizzaapp/customer_welcome.html', context)


def user_logout(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    logout(request)
    return redirect('userloginpage')


def place_order(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    username = request.user.username
    phoneno = CustomerModel.objects.filter(userid=request.user.id)[0].phoneno
    address = request.POST['address']
    ordered_items = ""
    for pizza in PizzaModel.objects.all():
        pizzaid = pizza.id
        name = pizza.name
        price = pizza.price
        quantity = request.POST.get(str(pizzaid), " ")
        if str(quantity) != "0" and str(quantity) != " ":
            ordered_items = ordered_items + "NAME: " + name + " PRICE: " + str(
                int(quantity) * float(price)) + " QUANTITY: " + quantity + "     "
    OrderModel(username=username, phoneno=phoneno, address=address, ordered_items=ordered_items).save()
    messages.add_message(request, messages.SUCCESS, "Order Successfully Placed!")
    return redirect('customerpage')


def user_orders(request):
    orders = OrderModel.objects.filter(username=request.user.username)
    context = {'orders': orders}
    return render(request, 'pizzaapp/user_orders.html', context)
