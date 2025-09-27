from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import NGO, Restaurant, CustomUser
from base.models import Orders
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy import distance
from django.db.models import Sum, F


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
            messages.error(request, "Password and Confirm Password do not match")
            return redirect("restaurant_signup")

        try:
            geolocator = Nominatim(user_agent="savr")
            address = name + ", " + location
            loc = geolocator.geocode(address)
            latitude = loc.latitude
            longitude = loc.longitude
        except:
            messages.error(request, "Couldn't find your address")
            return redirect("restaurant_signup")

        rest = Restaurant(
            name=name,
            location=location,
            email=email,
            phone=phone,
            fssai=fssai,
            latitude=latitude,
            longitude=longitude,
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

        try:
            geolocator = Nominatim(user_agent="savr")
            loc = geolocator.geocode(location)
            latitude = loc.latitude
            longitude = loc.longitude
        except:
            messages.error(request, "Couldn't find your address")
            return redirect("ngo_signup")

        ngo = NGO(
            name=name,
            location=location,
            email=email,
            ngoid=ngoid,
            latitude=latitude,
            longitude=longitude,
        )
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

            donation_history = self.request.user.rest.orders_set.filter(status="Clcd")
            context["donation_history"] = donation_history

            no_of_meals_donated = self.request.user.rest.orders_set.filter(
                status="Clcd"
            ).count()
            context["no_of_meals_donated"] = no_of_meals_donated

            no_of_donations_month = self.request.user.rest.orders_set.filter(
                status="Clcd", pickup_datetime__month=datetime.now().month
            ).count()
            context["no_of_donations_month"] = no_of_donations_month

            no_of_waste_reduced = (
                self.request.user.rest.orders_set.filter(status="Clcd").count() * 10
            )
            context["no_of_waste_reduced"] = no_of_waste_reduced
        elif request.user.type == "NGO":
            context = {}
            available_donations = Orders.objects.filter(status="Ld")

            donations = []
            for i in available_donations:
                lat1 = i.rest.latitude
                long1 = i.rest.longitude
                lat2 = request.user.ngo.latitude
                long2 = request.user.ngo.longitude
                dist = distance.distance((lat1, long1), (lat2, long2)).km
                donation = {
                    "rest": i.rest,
                    "qty": i.qty,
                    "pickup_datetime": str(i.pickup_datetime),
                    "location": i.rest.location,
                    "dish": i.dish,
                    "distance": round(dist, 2),
                    "id": i.id,
                }
                donations.append(donation)
            donations = sorted(donations, key=lambda x: x["distance"])

            context["available_donations"] = donations

            active_pickups = self.request.user.ngo.orders_set.filter(status="Clmd")
            context["active_pickups"] = active_pickups

            no_of_meals_recieved = self.request.user.ngo.orders_set.filter(
                status="Clcd"
            ).count()
            context["no_of_meals_recieved"] = no_of_meals_recieved

            no_of_pickups_month = self.request.user.ngo.orders_set.filter(
                status="Clcd", pickup_datetime__month=datetime.now().month
            ).count()
            context["no_of_pickups_month"] = no_of_pickups_month

            no_of_rest = (
                self.request.user.ngo.orders_set.filter(
                    status="Clcd",
                )
                .values("rest")
                .distinct()
                .count()
            )
            context["no_of_rest"] = no_of_rest

        return render(request, self.template, context)


def logoutView(request):
    logout(request)
    return redirect("main_page")


@login_required
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


@login_required
def UpdateFoodDonation(request):
    if request.method == "POST":
        editing_id = request.POST.get("editingId")
        dish = request.POST.get("dish")
        qty = request.POST.get("quantity")
        pickup_datetime = request.POST.get("pickup_time")
        pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%dT%H:%M")

        order = Orders.objects.get(id=editing_id)
        if order.rest != request.user.rest:
            return HttpResponseForbidden("You cannot edit other users' order")

        order.dish = dish
        order.qty = qty
        order.pickup_datetime = pickup_datetime
        order.save()

        return JsonResponse({"success": True})


@login_required
def ClaimFoodView(request, pk):
    order = Orders.objects.get(id=pk)
    order.claimed_ngo = request.user.ngo
    order.status = "Clmd"
    order.save()

    return redirect("dashboard")


@login_required
def PickedFoodView(request, pk):
    order = Orders.objects.get(id=pk)
    order.status = "Clcd"
    order.save()

    return redirect("dashboard")


@login_required
def DltFoodView(request, pk):
    order = Orders.objects.get(id=pk)
    if order.rest != request.user.rest:
        return HttpResponseForbidden("You cannot delete other users' order")

    order.delete()
    return redirect("dashboard")


class LeaderboardView(LoginRequiredMixin, View):
    template="accounts/leaderboards.html"

    def get(self, request):
        top_restaurants_monthly = Orders.objects.filter(status="Clcd", pickup_datetime__month=datetime.now().month).values('rest__name').annotate(total_qty=Sum('qty')).order_by('-total_qty')
        top_ngos_monthly = Orders.objects.filter(status="Clcd", pickup_datetime__month=datetime.now().month).values('claimed_ngo__name').annotate(total_qty=Sum('qty')).order_by('-total_qty')

        top_restaurants_all_time = Orders.objects.filter(status="Clcd").values('rest__name').annotate(total_qty=Sum('qty')).order_by('-total_qty')
        top_ngos_all_time = Orders.objects.filter(status="Clcd").values('claimed_ngo__name').annotate(total_qty=Sum('qty')).order_by('-total_qty')

        context={'current_month_name': datetime.now().strftime("%B"), 'top_restaurants_monthly': top_restaurants_monthly, 'top_ngos_monthly': top_ngos_monthly, 'top_restaurants_all_time': top_restaurants_all_time, 'top_ngos_all_time': top_ngos_all_time}

        return render(request, self.template, context)
