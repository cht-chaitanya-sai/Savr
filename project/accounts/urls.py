from django.urls import path, include
from . import views

urlpatterns = [
    path('rest_signup/', views.RestSignUpView.as_view(), name="restaurant_signup"),
    path('ngo_signup/', views.NGOSignUpView.as_view(), name="ngo_signup"),
    path('login/', views.LoginView.as_view(), name="login"),

]