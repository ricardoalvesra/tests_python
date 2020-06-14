from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Customer
from django.db.models import Avg, Max, Min
from django.core import serializers

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'sales/login.html', {'message': None})
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'sales/index.html', context)


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'sales/login.html', {'message': 'Invalid credentials.', 'is_authenticated': request.user.is_authenticated})


def logout_view(request):
    logout(request)
    return render(request, 'sales/login.html', {'message': 'Logged out.', 'is_authenticated': request.user.is_authenticated})


def customers(request):
    if not request.user.is_authenticated:
        return render(request, 'sales/login.html', {'message': None})

    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'sales/customers.html', context)


def customer(request):
    if not request.user.is_authenticated:
        return render(request, 'sales/login.html', {'message': None})
    if request.method == 'POST':
        customer = Customer()

        if request.POST["pk"] != '':
            customer.pk = request.POST["pk"]

        customer.name = request.POST['name']
        customer.address = request.POST['address']
        customer.postalcode = request.POST['postalcode']
        customer.county = request.POST['county']
        customer.telephone = request.POST['telephone']
        customer.email = request.POST['email']
        customer.save()

        context = {
            'user': request.user,
            'is_authenticated': request.user.is_authenticated
        }
        return HttpResponseRedirect(reverse('customers'))
    else:
        context = {
            'user': request.user,
            'is_authenticated': request.user.is_authenticated
        }
        return render(request, 'sales/customer.html', context)


def customer_by_id(request, customer_id):
    if not request.user.is_authenticated:
        return render(request, 'sales/login.html', {'message': None})

    customer = Customer.objects.get(pk=customer_id)

    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'customer': customer
    }
    return render(request, 'sales/customer.html', context)


def delete_customer(request):
    Customer.objects.filter(pk=request.POST['pk']).delete()
    return HttpResponseRedirect(reverse('customers'))


def get_customers(request):
    customers = Customer.objects.all()
    return JsonResponse(serializers.serialize('json', customers), safe=False)
