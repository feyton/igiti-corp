from .forms import SignUpForm
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from forestry.models import BlogPost
from store.models import SeedProduct
from django.views.generic import View
from .models import SignUp, ErrorReport
from django.contrib import messages
from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator


@method_decorator(require_GET, name='dispatch')
class HomeView(View):
    def get(self, *args, **kwargs):
        context = {
            'blog': BlogPost.objects.filter(published=True).order_by('-created')[:5],
            'seed': SeedProduct.objects.filter(available=True)

        }
        return render(self.request, 'index.html', context)


home = HomeView.as_view()


def species(request):
    return redirect('forestry')


def terms(request):
    return render(request, 'pages/terms.html')


def privacy(request):
    return render(request, 'pages/privacy.html')


@require_POST
def subscribe(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        form.save()

        # signup.save()
        subject = 'Welcome to Igiti Corp'
        message = 'Thank you for subscribing to our weekly newsletter'
        recepient = email
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [recepient], fail_silently=True)

        messages.success(request, 'You have subscribed successfully')
        return redirect("home")

        #
    elif not form.is_valid() and request.POST['email'] is not None:
        return HttpResponse('Sorry, You are already subscribed. <br>Thank You. <br><br><a href="/">GO HOME</a>')

    else:
        messages.error(request, 'Fill all fields in form')
        return redirect('home')


@require_POST
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
                      message, settings.EMAIL_HOST_USER, [recipient], fail_silently=True)

        report = ErrorReport()
        report.email = email
        report.url = str(url)
        report.sender_ip = sender_ip
        report.message = str(message)
        report.spam = spam
        report.save()

        messages.success(request, 'Thank you for the update!!!')
        return redirect('home')
    else:
        return redirect('home')
