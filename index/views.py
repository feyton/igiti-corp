from django.shortcuts import render, redirect
from forestry.models import Category, BlogPost
from django.http import HttpResponse
from .models import SignUp


def home(request):
    context = {
        'blog': BlogPost.objects.filter(published=True),
        # 'seed': SeedProduct.objects.filter(available= True)
        
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
        if SignUp.objects.filter(email=email).exists():
            return HttpResponse('<p> Email already used</P>')
        else:
            new = SignUp()
            new.full_name = name
            new.email = email
            new.save()
            context = {
                'name': name,
                'email': email
            }
            return render(request, 'success/sub.html', context)
    else:
        return redirect('home')