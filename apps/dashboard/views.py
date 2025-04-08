from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View


# Create your views here.

class PrivacyPolicyView(TemplateView):
    template_name = 'dashboard/privacy_policy.html'


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class Index2View(View):
    def get(self, request):
        return render(request, 'index2.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'contact_us.html')