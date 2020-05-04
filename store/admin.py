from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import *


# FUNCTIONS
def set_available(ModelAdmin, request, queryset):
    queryset.update(available = 'True')

set_available.short_description = 'Set selected as available'

def rm_available(ModelAdmin, request, queryset):
    queryset.update(available = 'False')

rm_available.short_description = 'Make unavailable'

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'



# CHANGING HEADER
admin.site.site_header = 'Igiti Corp'


# REGISTERING MODELS
@admin.register(SeedProduct)
class TreeSeedAdmin(admin.ModelAdmin):
    list_display    = ('scientific_name', 'price', 'available')
    list_filter     = ('available',)
    actions         = [set_available, rm_available]
    fieldsets = (
        ('BASIC INFORMATION', {
            'fields': ('scientific_name', 'common_name')
        }),(
        'PRODUCT INFORMATION', {
            'fields': ('image1', 'price', 'discount_price', 'image2')
        }),
        ('STORE STATUS', {
            'fields' : ('category', 'available', 'recommended', 'pre_treatment')
        }),
        ('OTHERS', {'fields': ('plantation_districts', 'seeds_kg', 'germination_rate', 'seed_source', 'short_note')})
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    # 'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        # 'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'district',
        'country',
        # 'address_type',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'street_address', 'apartment_address']



admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)

admin.site.register(SeedPretreatment)
admin.site.register(District)
admin.site.register(TypesOfSeed)


