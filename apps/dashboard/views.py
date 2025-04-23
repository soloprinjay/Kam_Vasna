import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from apps.dashboard.models import Contact
from django.http import JsonResponse
from django.contrib import messages


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
