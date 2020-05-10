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
from .forms import (CreateUserForm, UpdateAddressForm, UpdateProfileForm,
                    UpdateUserForm)
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
        orders = Order.objects.filter(user=user)
        context = {
            'orders': orders,
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
        user = self.request.user
        address, created = Address.objects.get_or_create(
            user=user, address_type='S', default=True)
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=profile)
        address_form = UpdateAddressForm(instance=address)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'address_form': address_form,
            'profile': profile,
            'active': 'profile',
            'address': address
        }
        return render(self.request, 'dashboard/pages/user.html', context)

    def post(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        user = self.request.user
        address = Address.objects.get(
            user=user, address_type='S', default=True)
        user_form = UpdateUserForm(self.request.POST, instance=user)
        profile_form = UpdateProfileForm(
            self.request.POST, self.request.FILES, instance=profile)
        address_form = UpdateAddressForm(self.request.POST, instance=address)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'address_form': address_form,
            'profile': profile,
            'active': 'profile',
            'address': address
        }
        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            # FORM DATA
            user_form.save()
            profile_form.save()
            address_form.save()

            messages.info(
                self.request, 'Your profile was updated successfully')
            return redirect('update-profile')
        messages.info(self.request, 'Please fill in all information')
        return render(self.request, 'dashboard/pages/user.html', context)



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
