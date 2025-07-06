import json
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
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
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                email = data.get('email')
            except json.JSONDecodeError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid JSON data.'
                }, status=400)
        else:
            email = request.POST.get('email')

        if not email:
            return JsonResponse({
                'status': 'error',
                'message': "Please enter a valid email address."
            }, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'status': 'error',
                'message': "Invalid email address."
            }, status=400)

        if Subscription.objects.filter(email=email).exists():
            return JsonResponse({
                'status': 'info',
                'message': "You're already subscribed with this email."
            }, status=200)

        Subscription.objects.create(email=email)
        return JsonResponse({
            'status': 'success',
            'message': "Congratulations, you are now one of our members!"
        }, status=201)


class PrivacyPolicyView(View):
    def get(self, request):
        return render(request, 'privacy_policy.html')
