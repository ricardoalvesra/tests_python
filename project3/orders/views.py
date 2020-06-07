from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import RegisterForm, ProductCategory, Product, ProductExtra, PriceList, Order
from django.db.models import Avg, Max, Min

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': None})
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.username == 'admin'
    }
    return render(request, 'orders/user.html', context)


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if request.user.username == 'admin':
            return HttpResponseRedirect(reverse('orders'))
        else:
            return HttpResponseRedirect(reverse('menu'))
    else:
        return render(request, 'orders/login.html', {'message': 'Invalid credentials.', 'is_authenticated': request.user.is_authenticated })


def logout_view(request):
    logout(request)
    return render(request, 'orders/login.html', {'message': 'Logged out.', 'is_authenticated': request.user.is_authenticated})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, 'orders/register.html', {'form': form, 'is_authenticated': request.user.is_authenticated, 'is_admin': request.user.username == 'admin'})


def menu(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': None})

    order = []
    if request.session.has_key('order'):
        order = request.session.get('order')

    if request.method == 'POST':
        extras = []
        for item in request.POST.getlist('extra'):
            extras.append(int(item))

        order.append({
            'product': int(request.POST['product']),
            'size': int(request.POST['size']),
            'extras': extras,
            'quantity': int(request.POST['quantity'])
        })

        request.session['order'] = order

    context = {
        'user': request.user,
        'menu': build_menu(),
        'order': build_my_order(order),
        'is_authenticated': request.user.is_authenticated
    }

    return render(request, 'orders/menu.html', context)


def get_min_price(productid):
    priceformatted = ''
    price = PriceList.objects.filter(
        product_id=productid).aggregate(Min('price'))['price__min']
    if price is not None:
        priceformatted = '$ ' + '{0:.2f}'.format(price)
    return priceformatted


def build_menu():
    menu = []

    categories = ProductCategory.objects.all()
    for category in categories:
        menuitem = {
            'categoryid': category.id,
            'category': category.name,
            'products': []
        }

        products = Product.objects.filter(productcategory_id=category.id)

        for product in products:
            prices = list(PriceList.objects.filter(product_id=product.id))
            extras = list(ProductExtra.objects.filter(
                productcategory_id=category.id))

            menuitem['products'].append(
                {
                    'id': product.id,
                    'name': product.name,
                    'hasExtra': product.hasExtra,
                    'from': get_min_price(product.id),
                    'prices': prices,
                    'extras': extras
                }
            )

        menu.append(menuitem)

    return menu


def build_my_order(order):
    myorder = {
        'items': [],
        'total': 0
    }
    i = 0
    for item in order:
        orderitem = {
            'id': i,
            'description': ''
        }

        # get product detail
        product = Product.objects.get(pk=item['product'])
        size = PriceList.objects.get(pk=item['size'])
        extras = []
        for i in item['extras']:
            extras.append(ProductExtra.objects.get(pk=i).name)

        # description
        orderitem['description'] = str(str(
            item['quantity']) + ' - ' + product.productcategory.name + ' ' + product.name + ' ' + size.size)
        if len(extras) > 0:
            separator = ', '
            orderitem['description'] += ' (' + separator.join(extras) + ')'
        orderitem['description'] += ' - ' + str(size.price * item['quantity'])

        myorder['items'].append(orderitem)
        myorder['total'] += size.price * item['quantity']

    return myorder


def removeitem(request):
    order = request.session.get('order')
    order.pop(int(request.POST["item"]))
    request.session['order'] = order

    return HttpResponseRedirect(reverse('menu'))


def confirmation(request):
    order = request.session.get('order')
    myorder = build_my_order(order)

    newOrder = Order()
    newOrder.customer = request.user
    for item in myorder['items']:
        newOrder.description += item["description"] + '; '
    newOrder.total = myorder['total']
    newOrder.status = 'Open'
    newOrder.save()

    request.session.pop('order')

    context = {
        'order': build_my_order(order),
        'orderid': newOrder.pk,
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.username == 'admin'
    }

    return render(request, 'orders/confirmation.html', context)


def orders(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': None})

    if request.user.username != 'admin':
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'GET':
        orders = Order.objects.exclude(status='Delivered')
        context = {
            'orders': orders,
            'is_authenticated': request.user.is_authenticated,
            'is_admin': request.user.username == 'admin'
        }
        return render(request, 'orders/orders.html', context)
    else:
        order = Order.objects.get(pk=int(request.POST["item"]))
        order.status = request.POST["status"]
        order.save()

        return HttpResponseRedirect(reverse('orders'))
