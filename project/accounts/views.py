from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import NGO, Restaurant, CustomUser
from base.models import Orders
from django.http import HttpResponse, JsonResponse
from datetime import datetime


class RestSignUpView(View):
    template = "accounts/rest_signup.html"
    model = Restaurant

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        name = request.POST.get("restaurant-name")
        location = request.POST.get("address")
        email = request.POST.get("email")
        phone = request.POST.get("phone-number")
        fssai = request.POST.get("fssai")
        password1 = request.POST.get("password")
        password2 = request.POST.get("confirm-password")
        passwd = False
        if password1 == password2:
            passwd = True
        else:
            return HttpResponse("Error")

        rest = Restaurant(
            name=name, location=location, email=email, phone=phone, fssai=fssai
        )
        rest.save()

        user = CustomUser(username=email, email=email, type="Rest", rest=rest)
        user.set_password(password1)
        user.save()

        return redirect("login")


class NGOSignUpView(View):
    template = "accounts/ngo_signup.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        name = request.POST.get("ngo-name")
        location = request.POST.get("address")
        email = request.POST.get("email")
        ngoid = request.POST.get("reg-id")
        password1 = request.POST.get("password")
        password2 = request.POST.get("confirm-password")
        passwd = False
        if password1 == password2:
            passwd = True
        else:
            return HttpResponse("Error")

        ngo = NGO(name=name, location=location, email=email, ngoid=ngoid)
        ngo.save()

        user = CustomUser(username=email, email=email, type="NGO", ngo=ngo)
        user.set_password(password1)
        user.save()

        return redirect("login")


class LoginView(View):
    template = "accounts/login.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return HttpResponse("Error")


class DashboardView(LoginRequiredMixin, View):
    template = "accounts/dashboard.html"

    def get(self, request):
        context = {}
        if request.user.type == "Rest":
            active_donations = self.request.user.rest.orders_set.filter(
                status__in=["Ld", "Clmd"]
            )
            context["active_donations"] = active_donations

            donation_history=self.request.user.rest.orders_set.filter(status="Clcd")
            context['donation_history']=donation_history
        elif request.user.type == "NGO":
            context = {}
            available_donations = Orders.objects.filter(status="Ld")
            context["available_donations"] = available_donations

            active_pickups=self.request.user.ngo.orders_set.filter(status="Clmd")
            context['active_pickups'] = active_pickups
        return render(request, self.template, context)


def logoutView(request):
    logout(request)
    return redirect("main_page")


def ListFoodDonation(request):
    if request.method == "POST":
        dish = request.POST.get("dish")
        qty = request.POST.get("quantity")
        pickup_datetime = request.POST.get("pickup_time")
        pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%dT%H:%M")
        rest = request.user.rest

        order = Orders(dish=dish, qty=qty, rest=rest, pickup_datetime=pickup_datetime)
        order.save()

        return JsonResponse({"success": True})
    
def ClaimFoodView(request, pk):
    order=Orders.objects.get(id=pk)
    order.claimed_ngo=request.user.ngo
    order.status="Clmd"
    order.save()

    return redirect("dashboard")

def PickedFoodView(request, pk):
    order=Orders.objects.get(id=pk)
    order.status="Clcd"
    order.save()

    return redirect("dashboard")