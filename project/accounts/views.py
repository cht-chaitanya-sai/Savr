from django.shortcuts import render
from django.views import View

# Create your views here.
class RestSignUpView(View):
    template="accounts/rest_signup.html"

    def get(self, request):
        return render(request, self.template)
    

class NGOSignUpView(View):
    template="accounts/ngo_signup.html"

    def get(self, request):
        return render(request, self.template)

class LoginView(View):
    template="accounts/login.html"

    def get(self, request):
        return render(request, self.template)