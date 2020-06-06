from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import RegisterForm, ProductCategory, Product, ProductExtra, PriceList, Order, OrderItem
from django.db.models import Avg, Max, Min

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "orders/user.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("menu"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisterForm()

    return render(response, "orders/register.html", {"form":form})

def menu(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    menu = []

    categories = ProductCategory.objects.all()
    for category in categories:
        menuitem = {
            "categoryid": category.id,
            "category" : category.name,
            "products" : []
        }

        products = Product.objects.filter(productcategory_id = category.id)
        
        for product in products:
            prices = list(PriceList.objects.filter(product_id = product.id))
            extras = list(ProductExtra.objects.filter(productcategory_id = category.id))

            menuitem["products"].append(
                { 
                    "id": product.id,
                    "name": product.name,
                    "hasExtra":product.hasExtra,
                    "from": get_min_price(product.id),
                    "prices": prices,
                    "extras": extras
                }
            )
      
        menu.append(menuitem)

    context = {
        "user": request.user,
        "menu": menu
    }

    return render(request, "orders/menu.html", context)

def additem(request):
    return menu(request)

def get_min_price(productid):
    priceformatted = ''
    price = PriceList.objects.filter(product_id=productid).aggregate(Min('price'))['price__min']
    if price is not None:
        priceformatted = '$ ' + '{0:.2f}'.format(price)
    return priceformatted

