from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from forestry.models import BlogPost
from store.models import SeedProduct

from .models import SignUp, ErrorReport


def home(request):
    context = {
        'blog': BlogPost.objects.filter(published=True),
        'seed': SeedProduct.objects.filter(available=True)

    }
    return render(request, 'index.html', context)


def species(request):
    return redirect('forestry')


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


def subscribe(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        new = SignUp()
        try:
            new.full_name = name
            new.email = email
            new.save()
            subject = 'Welcome to Igiti Corp'
            message = 'Thank you for subscribing to our weekly newsletter'
            recepient = email
            send_mail(subject,
                      message, settings.EMAIL_HOST_USER, [recepient], fail_silently=True)
            context = {
                'name': name,
                'email': email
            }

            return render(request, 'success/sub.html', context)
        except Exception as e:
            return HttpResponse('Sorry, You are already subscribed. <br>Thank You. <br><br><a href"/">GO HOME</a>')
    else:
        return redirect('home')


def error(request):
    if request.method == 'POST':
        sender_ip = request.META['REMOTE_ADDR']
        url = request.META['HTTP_REFERER']
        if not request.user.is_authenticated:
            email = request.POST['email']

        else:
            email = request.user.email

        message = request.POST['message']
        if len(message) <= 20:
            success = """Your message was not clear<br> but we really appreciate your update.
            <br> The message must contain at least 20 characters <br><br>"""
            spam = True
        else:
            success = """
            Thank you for the report. We appreciate it. <br>
            We will get back to you as soon as possible.<br> <br>
            """
            spam = False
            subject = 'Error report from Igiti Corp'
            recipient = 'tumbafabruce@gmail.com'
            send_mail(subject,
                      message, settings.EMAIL_HOST_USER, [recepient], fail_silently=True)

        report = ErrorReport()
        report.email = email
        report.url = str(url)
        report.sender_ip = sender_ip
        report.message = str(message)
        report.spam = spam
        report.save()

        context = {
            'email': email,
            'message': success
        }
        return render(request, 'success/simple.html', context)
    else:
        return redirect('home')
