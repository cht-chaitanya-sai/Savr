from django.urls import path
from . import views

urlpatterns = [
    path("rest_signup/", views.RestSignUpView.as_view(), name="restaurant_signup"),
    path("ngo_signup/", views.NGOSignUpView.as_view(), name="ngo_signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("list_food_donation/", views.ListFoodDonation, name="list_food"),
    path("update_food_donation/", views.UpdateFoodDonation, name="update_food"),
    path("claim_food/<int:pk>/", views.ClaimFoodView, name="claim_food"),
    path("picked_food/<int:pk>/", views.PickedFoodView, name="picked_food"),
    path("dlt_food/<int:pk>/", views.DltFoodView, name="dlt_food"),
]
