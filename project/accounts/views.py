from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from .models import NGO, Restaurant, CustomUser


# Create your views here.
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
            return

        rest = Restaurant(
            name=name, location=location, email=email, phone=phone, fssai=fssai
        )
        rest.save()

        user = CustomUser(username=email, email=email)
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
            return

        ngo = NGO(name=name, location=location, email=email, ngoid=ngoid)
        ngo.save()

        user = CustomUser(username=email, email=email)
        user.set_password(password1)
        user.save()

        return redirect("login")


class LoginView(View):
    template = "accounts/login.html"

    def get(self, request):
        return render(request, self.template)

