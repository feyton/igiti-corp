from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from store.forms import AddProductForm
from store.models import Address, Order, SeedProduct

from .decorators import staff_only
from .forms import CreateUserForm, UpdateUserForm
from .models import UserProfile

User = get_user_model()

staff = [login_required, staff_only]

def update_data(values):
    update = True
    for field in values:
        if field == '':
            update = False
    return update



@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    def get(self, *args, **kwargs):
        context ={
            'active': 'dashboard'
        }
        return render(self.request, 'dashboard/index.html', context)
            
    def post(self, *args, **kwargs):
        pass


@method_decorator(staff, name='dispatch')
class AdminView(View):
    def get(self, *args, **kwargs):
        return redirect('/123FEYTON')

    def post(self, *args, **kwargs):
        pass



@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        # orders = Order.objects.filter(user=user)
        context = {
            # 'orders': orders,
            'active': 'orders'
        }

        return render(self.request, 'dashboard/pages/orders.html', context)


@method_decorator(login_required, name='dispatch')
class Notification(View):
    def get(self, *args, **kwargs):
        context = {
            'active': 'notification'
        }
        return render(self.request, 'dashboard/pages/notifications.html', context)

    def post(self, *args, **kwargs):
        pass


@method_decorator(staff, name='dispatch')
class ProductView(View):
    def get(self, *args, **kwards):
        user = self.request.user
        orders = Order.objects.all()
        products = SeedProduct.objects.all()
        form = AddProductForm
        context = {
            'active': 'product',
            'orders': orders,
            'products': products,
            'form': form
        }
        return render(self.request, 'dashboard/pages/product.html', context)

    def post(self, *args, **kwargs):
        form = AddProductForm(self.request.POST, self.request.FILES or None)
        if form.is_valid:
            form.save()
            messages.warning(self.request, 'New Product Added')
            return redirect('product')
        
        return redirect('product')

@login_required
@staff_only
def edit_product(request, pk):
    product = SeedProduct.objects.get(id=pk)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Product Updated')

            return redirect('product')

        return redirect('product')

    form = AddProductForm(instance=product)
    context = {
        'active': 'product',
        'form': form,
        'product': product,
    }

    return render(request, 'dashboard/pages/change.html', context)


@method_decorator(login_required, name='dispatch')
class UpdateProfileView(View):
    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
            
        form = UpdateUserForm(instance=profile)
        address = Address.objects.get_or_create(user=self.request.user, address_type='S', default=True)
    
        context = {
            'form': form,
            'profile': profile,
            'active': 'profile',
            'address': address[0]
        }
        return render(self.request, 'dashboard/pages/user.html', context)

    def post(self, *args, **kwargs):
        form = UpdateUserForm(self.request.POST, self.request.FILES or None)
        if form.is_valid():
            # FORM DATA
            user = self.request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            district = form.cleaned_data.get('district')
            street = form.cleaned_data.get('street_address')
            bio = form.cleaned_data.get('biography')
            files = form.cleaned_data.get('profile_image')

            # DATABASE
            address_old = Address.objects.get(
                user=self.request.user, address_type='S', default=True)

            address_old.street_address = street
            address_old.city = city
            address_old.first_name = first_name
            address_old.last_name = last_name
            address_old.district = district
            if update_data([country]):
                address_old.country = country
            address_old.save()

            user.first_name = first_name
            user.last_name = last_name
            user.save()
            profile = UserProfile.objects.get(user=self.request.user)
            profile.biography = bio
            if 'profile_image' in self.request.FILES:
                profile.image = files
            profile.save()

            messages.info(
                self.request, 'Your profile was updated successfully')
            return redirect('update-profile')

        return render(self.request, 'dashboard/pages/user.html', {'form': form})

# API CALSS
def get_data(request, *args, **kwargs):
    labels = ['Products', 'User']
    data_default = [SeedProduct.objects.all().count(),
                    User.objects.all().count()]
    data = {
        'labels': labels,
        'data_default': data_default,
    }
    return JsonResponse(data)


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ['Products', 'User', 'May']
        data_default = [SeedProduct.objects.all().count(),
                        User.objects.all().count(), 4]
        data = {
            'labels': labels,
            'data_default': data_default,
        }

        return Response(data)
