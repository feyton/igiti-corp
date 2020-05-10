from django.urls import path

from user.views import edit_product

from .views import (AddCouponView, CheckoutView, HomeView, OrderSummaryView,
                    PaymentView, RequestRefundView, SeedProductDetailView,
                    TreeSeedDetailView, TreeSeedListView, add_to_cart,
                    delete_product, download_pdf, generate_card,
                    remove_from_cart, remove_single_item_from_cart, order_detail)

app_name = 'store'

urlpatterns = [
    # path('', TreeSeedListView.as_view(), name='list_seeds'),
    # path('<slug>', TreeSeedDetailView.as_view(), name='detail_seed'),
    path('', HomeView.as_view(), name='store'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', SeedProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('generate-card/<slug>', generate_card, name='generate-card'),
    path('download/pdf/<slug>/', download_pdf, name='download-pdf'),
    path('edit-product/<pk>/', edit_product, name='edit_product'),
    path('delete-product/<pk>', delete_product, name='delete_product'),
    path('order-detail/<pk>/', order_detail, name='order-detail'),
]
