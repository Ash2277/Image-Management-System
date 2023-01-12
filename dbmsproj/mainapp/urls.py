
from django.urls import path
# from django.contrib.auth import views
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user"),
    path('account_settings/', views.accountSettings, name="account"),
    path('', views.home, name="home"),
    path('images/', views.images, name="images"),
    path('customer/<int:pk>/', views.customer, name="customer"),
    path('create_order/<int:pk>/', views.createOrder, name="create_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete-order"),
]
