from ast import Or
import imp
import re
from statistics import quantiles
from unicodedata import name
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import is_valid_path
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MangaForm, editForm, RegForm, LoginForm, EditUserForm, MangaAddCartForm, OrderCreateForm
from .models import Manga, OrderItem, User, Order, OrderItem
from .cart import Cart
from django.contrib.auth import hashers

# Create your views here.

# получение данных (просмотр) из бд - все пользователи
def home(request):
    try:
        role = request.session['role']
        role_login = request.session['role_login']
    except:
        role = 0
        role_login = 0
    price = request.POST.get("search_by_price")
    if price is "":
        manga_list = Manga.objects.get_queryset().order_by('id')
    else:
        manga_list = Manga.objects.filter(price=price).order_by('price')
    paginator = Paginator(manga_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj, 'role':role, 'role_login':role_login})


# добавлять данные в бд - администратор с ролью 1 или авторизированный пользователь с ролью 10 
def add(request):
    try:
        role = request.session['role']
    except:
        role = 0
    if role !=0:
        if request.method == "GET":
            userForm = MangaForm()
            return render(request, "addManga.html", {"form":userForm})
        elif request.method == "POST": # сохранение данных в бд
            manga = Manga()
            manga.name = request.POST.get("name")
            manga.author = request.POST.get("author")
            manga.price = request.POST.get("price")
            manga.save()
            return redirect("home")
    else:
        return redirect("home")


# редактирование данных в бд - только администратор с ролью 1
def edit(request, id):  
    print(request)
    try:
        role = request.session['role']
    except:
        role = 0
    if role ==1:
        try:
            manga = Manga.objects.get(id=id)
            if request.method == "GET":
                userForm = editForm(
                    initial={
                        "name":manga.name,
                        "author":manga.author,
                        "price":manga.price})
                userForm.name = manga.name
                userForm.author = manga.author
                userForm.price = manga.price
                return render(request, "editManga.html", {"form":userForm})
            elif request.method == "POST":
                manga.name = request.POST.get("name")
                manga.author = request.POST.get("author")
                manga.price = request.POST.get("price")
                manga.save()
                return redirect("home")
        except Manga.DoesNotExist:
            return HttpResponseNotFound("<h2>Manga not found</h2>")
    else:
        return redirect("home")


# удаление данных из бд - только администратор с ролью 1
def delete(request, id):
    try:
        role = request.session['role']
    except:
        role = 0
    if role ==1:
        try:
            manga = Manga.objects.get(id=id)
            manga.delete()
            return HttpResponseRedirect("/")
        except Manga.DoesNotExist:
            return HttpResponseNotFound("<h2>Manga not found</h2>")
    else:
        return redirect("home")


def user_reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = User()
            user.name = request.POST.get("name")
            user.login = request.POST.get("login")
            user.role = 10 # простой пользователь, зарегистрированный по умолчанию
            #user.role = 1 # администратор
            user.password = hashers.make_password(request.POST.get("password"))

            user.mail = request.POST.get("mail")
            user.save()
            return redirect("home")
        else:
            return HttpResponse('such username already exists, invalid e-mail address or incorrect password entered')
    else:
        form = RegForm()
    return render(request, "reg.html", {'form':form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            temp_user = User()
            temp_user.password = request.POST.get("password")
            temp_user.login = request.POST.get("login")
            user = User.objects.get(login = temp_user.login)
            if (hashers.check_password(temp_user.password, user.password)):
                request.session['role'] = user.role
                request.session['role_login'] = user.login
            else:
                return HttpResponse("Your username and password didn't match.")
            return HttpResponseRedirect('/')
        else:
             return HttpResponse('incorrect password entered')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

def user_logout(request):
    try:
        del request.session['role']
        del request.session['role_login']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

def user_edit(request):
    try:
        role = request.session['role']
    except:
        role = 0
    if (role ==10 or role == 1):
        try:
            login = request.session['role_login']
            current_user = User.objects.get(login=login)
            temp_user = User()
            if request.method == "GET":
                userForm = EditUserForm(
                    initial={
                        "login":current_user.login,
                        "role":current_user.role,
                        "name":current_user.name,
                        "mail":current_user.mail,})
                userForm.login = current_user.login
                userForm.role = current_user.role
                userForm.name = current_user.name
                userForm.mail= current_user.mail
                userForm.new_password = current_user.password
                userForm.last_password = temp_user.password
                return render(request, "editUser.html", {"form":userForm})
            elif request.method == "POST":
                current_user.name = request.POST.get("name")
                current_user.mail = request.POST.get("mail")
                #temp_user = User()
                temp_user.password = request.POST.get("last_password")

                if (not temp_user.password):
                    current_user.save()
                    return redirect("home")
                elif (hashers.check_password(temp_user.password, current_user.password )):
                    current_user.password = hashers.make_password(request.POST.get('new_password'))
                    if (current_user.password):
                        current_user.save()
                    return redirect("home")
                else:
                    return HttpResponse("Your username and password didn't match.")
                #return HttpResponseRedirect('/')
                return redirect("home")
        except Manga.DoesNotExist:
            return HttpResponseNotFound("<h2>User not found</h2>")
    else:
        return redirect("home")

def add_manga_to_cart(request, id):  
    try:
        manga = Manga.objects.get(id=id)
        cart = Cart(request)
        if request.method == "GET":
            print(request)
            userForm = MangaAddCartForm( 
                initial={
                    "name":manga.name,
                    "author":manga.author,
                    "price":manga.price})
            userForm.name = manga.name
            userForm.author = manga.author
            userForm.price = manga.price
            return render(request, "addToCart.html", {"form":userForm})
        elif request.method == "POST":
            print(request)
            quantity = request.POST.get("quantity")
            #manga.name = request.POST.get("name")
            #manga.author = request.POST.get("author")
            #manga.price = request.POST.get("price")
            #manga.save()
            cart.add(manga=manga, quantity=quantity, update_quantity=['update'])
            return redirect("home")
    except Manga.DoesNotExist:
        return HttpResponseNotFound("<h2>Manga not found</h2>")

@require_POST
def cart_add(request, manga_id):
    cart = Cart(request)
    manga = get_object_or_404(Manga, id=manga_id)
    form = MangaAddCartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(manga=manga, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')

def cart_remove(request, manga_id):
    cart = Cart(request)
    manga = get_object_or_404(Manga, id=manga_id)
    cart.remove(manga)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = MangaAddCartForm(
            initial={'quantity':item['quantity'],
            'update':True})
    return render(request, 'detail.html', {'cart' :cart})

def order_create(request):
    try:
        role = request.session['role']
        role_login = request.session['role_login']
    except:
        role = 0
        role_login = 0
    if role !=0:
        cart = Cart(request)
        print(request)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            
            order=form.save()
            for item in cart:
                OrderItem.objects.create(order=order, manga=item['manga'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return redirect('home')
        else:
            form = OrderCreateForm(initial={"login":role_login})
            return render(request, 'create.html', {'cart':cart, 'form':form})
    else:
        return redirect("home")

def all_orders(request):
    try:
        role = request.session['role']
        role_login = request.session['role_login']
    except:
        role = 0
        role_login = 0
    if role !=0:
        #Получить все заказы для конкретного логина
        orders_list = Order.objects.filter(login=role_login).order_by('created')
        print("ORDERS LIST")
        print(orders_list)
        orders = []
        for order in orders_list:
            item_list = OrderItem.objects.filter(order__id=order.id)
            print("item list:")
            print(item_list)
            orders.append(item_list)
        items = OrderItem.objects.all()
        print(orders)
        return render(request, 'allOrders.html', {'order_list':orders_list, 'orders':orders, 'items':items})
    else:
        return redirect("home")


def validate_login(request):
    login = request.GET.get('login', None)
    response = {
        'is_taken': User.objects.filter(login=login).exists()
    }
    return JsonResponse(response)

def validate_email(request):
    email = request.GET.get('mail', None)
    response = {
        'is_taken': User.objects.filter(mail=email).exists()
    }
    return JsonResponse(response)