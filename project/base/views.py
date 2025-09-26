from django.shortcuts import render
from django.views import View


# Create your views here.
class MainPageView(View):
    template = "base/main.html"

    def get(self, request):
        return render(request, self.template)
