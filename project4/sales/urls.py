from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("customers", views.customers, name="customers"),
    path("getcustomers", views.get_customers, name="get_customers"),
    path("customer", views.customer, name="customer"),
    path("customer/<int:customer_id>", views.customer_by_id, name="customer_by_id"),
    path("delete_customer", views.delete_customer, name="delete_customer")
]
