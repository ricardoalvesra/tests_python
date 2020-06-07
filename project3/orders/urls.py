from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("menu", views.menu, name="menu"),
    path("removeitem", views.removeitem, name="removeitem"),
    path("confirmation", views.confirmation, name="confirmation"),
    path("orders", views.orders, name="orders")

]
