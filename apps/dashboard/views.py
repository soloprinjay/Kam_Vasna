import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.dashboard.models import Contact, Subscription


# Create your views here.

class ContactView(View):
    def get(self, request):
        return render(request, 'contact_us.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        if name and email and subject and message:
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            return JsonResponse({'status': 'success', 'message': 'Message sent successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please fill in all fields.'})


class UserSubscription(View):
    def post(self, request):
        email = request.POST.get('email')

        if email:
            if not Subscription.objects.filter(email=email).exists():
                Subscription.objects.create(email=email)
                messages.success(request, "Congratulations, you are now one of our members!")
            else:
                messages.info(request, "You're already subscribed with this email.")
        else:
            messages.error(request, "Please enter a valid email address.")

        return redirect('dashboard:stories')


class PrivacyPolicyView(View):
    def get(self, request):
        return render(request, 'privacy_policy.html')
