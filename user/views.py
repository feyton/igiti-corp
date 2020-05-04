from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from .forms import CreateUserForm



@login_required
def admin_view(request):
    return redirect("/feyton")

@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_staff:
            messages.info(self.request, 'Welcome admin')
            return redirect('owner')
        
        else:
            messages.info(self.request, 'Dashboard Comming soon. Stay connected')
            return redirect('home')
            
    def post(self, *args, **kwargs):
        pass

