from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import CreateUserForm, UpdateUserForm
from .models import UserProfile
from store.models import Address
from django.contrib.auth import get_user_model
from .decorators import staff_only

User = get_user_model()

staff = [login_required, staff_only]

@login_required
def admin_view(request):
    return redirect("/feyton")

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
        # user = self.request.user
        # orders = Order.objects.all()
        # products = SeedProduct.objects.all()
        # form = AddProductForm
        context = {
            'active': 'product',
            # 'orders': orders,
            # 'products': products,
            # 'form': form
        }
        return render(self.request, 'dashboard/pages/product.html', context)

    def post(self, *args, **kwargs):
        pass
        # form = AddProductForm(self.request.POST or None)
        # if form.is_valid:
        #     form.save()
        #     messages.warning(self.request, 'New Product Added')
        #     return redirect('notification')

        # else:
        #     return redirect('product')


@method_decorator(login_required, name='dispatch')
class UpdateProfileView(View):
    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
            
        form = UpdateUserForm(instance=profile)
        address = Address.objects.get_or_create(user=self.request.user, address_type='S')
    
        context = {
            'form': form,
            'profile': profile,
            'active': 'profile',
            'address': address
        }
        return render(self.request, 'dashboard/pages/user.html', context)

    def post(self, *args, **kwargs):
        form = UpdateUserForm(self.request.POST or None)
        if form.is_valid():
            # FORM DATA
            user = self.request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            # country = form.cleaned_data.get('country')
            # city = form.cleaned_data.get('city')
            # district = form.cleaned_data.get('district')
            # street = form.cleaned_data.get('street_address')
            bio = form.cleaned_data.get('biography')

            # DATABASE
            # address_old = Address.objects.get(
            #     user=self.request.user, address_type='S', default='True')
            # if address_old:
            #     print('Exists')
            #     address_old.street_address = street
            #     address_old.city = city
            #     address_old.first_name = first_name
            #     address_old.last_name = last_name
            #     address_old.district = district
            #     if update_data([country]):
            #         address_old.country = country
            #     address_old.save()

            user.first_name = first_name
            user.last_name = last_name
            user.save()
            profile = UserProfile.objects.get(user=self.request.user)
            profile.biography = bio
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
