from datetime import datetime
from django.db.models import Sum

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from user.models import UserProfile
from django_countries.fields import CountryField
from .utils import photo_path
User = get_user_model()


class District(models.Model):
    # CHOICES
    ecological_zones = (('HIGH', 'Highland'),
                        ('LOW', 'Lowlands'), ('Mid', 'Midlands'))

    # DATABASE FIELDS
    name = models.CharField(max_length=255, unique=True)
    ecelogical_zone = models.CharField(
        max_length=255, choices=ecological_zones, default='Mid')

    class Meta:
        verbose_name = 'district'
        verbose_name_plural = 'districts'
        ordering = ['name']

    # Functions
    def __str__(self):
        return self.name


class TypesOfSeed(models.Model):
    # CHOICES
    types = (('ORT', 'Orthodox'), ('RECAL', 'Recalcitrant'),
             ('SUB-OR', 'Sub-Orthodox'))
    storage = (
        ('RT', 'Room temperature'),
        ('CRT', 'Cold room temperature')
    )

    # DATABASE FIELDS
    name = models.CharField(max_length=100, choices=types)
    storage_type = models.CharField(
        _('storage type'), max_length=500, choices=storage)
    max_years = models.IntegerField(_('Max storage years'), blank=True)
    min_years = models.IntegerField(_('Min storage years'), blank=True)
    max_moisture = models.IntegerField(
        blank=True, verbose_name='Max Storage Moisture')
    min_moisture = models.IntegerField(
        blank=True, verbose_name='Min Storage Moisture')
    overview = RichTextUploadingField(_('overview'), blank=True, null=True)

    # FUNCTIONS

    class Meta:
        verbose_name = 'Seed Type'
        verbose_name_plural = 'Seed Types'

    def __str__(self):
        return self.name


class SeedPretreatment(models.Model):
    # CHOICES
    types_choice = (('MC', 'Mechanical'), ('CH', 'Chemical'))

    # DATABASE FIELDS

    title = models.CharField(max_length=255)
    types = models.CharField(
        max_length=255, choices=types_choice, default='MC')
    process = RichTextUploadingField(_('description'), blank=True)

    # FUNCTIONS

    class Meta:
        verbose_name = 'Seed Pre-Treatment'
        verbose_name_plural = 'Seed Pre-Treatments'

    def __str__(self):
        return '{} <{}>'.format(self.title, self.types)

    def get_absolute_url(self):
        pass


class SeedProduct(models.Model):
    folder = 'store'
    # CHOICES
    category_choice = (('FOR', 'Forestry'), ('AGR', 'Agroforestry'))
    # DATABASE FIELDS
    # BASIC INFO
    scientific_name = models.CharField(_('scientific name'), max_length=255)
    common_name = models.CharField(
        _('common name'), max_length=255, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    # UNIQUE LINK
    slug = AutoSlugField(
        _('slug'), populate_from='scientific_name', unique=True)
    # PROFILE
    image1 = models.ImageField(_('image1'), blank=True, null=True,
                               upload_to=photo_path, default="default/product_image1.jpg")
    image2 = models.ImageField(_('image2'), blank=True, null=True,
                               upload_to=photo_path, default="default/product_image2.jpg")
    plantation_districts = models.ManyToManyField(
        District, verbose_name='Plantation districts', blank=True)

    # CART DETAILS
    price = models.IntegerField(_('price'))
    discount_price = models.FloatField(_('discount'), blank=True, null=True)
    available = models.BooleanField(default=True)
    category = models.CharField(
        max_length=3, choices=category_choice, help_text='Choose one')
    recommended = models.BooleanField(default=False)

    # ADDITIONAL INFO CARD
    seeds_kg = models.IntegerField(_('Seeds per Kilogram'), blank=True)
    seed_type = models.ForeignKey(
        TypesOfSeed, on_delete=models.SET_NULL, null=True, blank=True)
    germination_rate = models.FloatField(verbose_name='Germination Rate')
    seed_source = models.CharField(
        max_length=255, verbose_name='Seed source', blank=True)
    short_note = models.TextField(
        _('Short description'), blank=True, null=True)
    pre_treatment = models.ForeignKey(
        SeedPretreatment, on_delete=models.SET_NULL, null=True, blank=True)

    # FUNCTIONS

    class Meta:
        verbose_name = 'Seed Product'
        verbose_name_plural = 'Seed Products'
        ordering = ['created_on']

    def __str__(self):
        return self.scientific_name

    def get_absolute_url(self):
        return reverse('store:product', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('store:add-to-cart', kwargs={'slug': self.slug})

    def remove_to_cart_url(self):
        return reverse('store:remove-from-cart', kwargs={'slug': self.slug})

    def generate_card_url(self):
        return reverse('store:generate-card', kwargs={'slug': self.slug})

    def get_discount_percent(self):
        if self.discount_price:
            discount = (self.price - self.discount_price) * 100 / self.price
            return int(discount)
        return 0

    def download_pdf_url(self):
        return reverse('store:download-pdf', kwargs={'slug': self.slug})

    def edit_url(self):
        return reverse('store:edit_product', kwargs={'pk': self.id})

    def delete_url(self):
        return reverse('store:delete_product', kwargs={'pk': self.id})


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(SeedProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.scientific_name}'

    def get_total_item_price(self):
        if self.item.discount_price:
            return self.quantity * self.item.discount_price
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        total = 0
        if self.item.discount_price:
            total = float(self.quantity) * self.item.discount_price
            return total
        return total

    def get_amount_saved(self):
        saved = 0
        if self.item.discount_price:
            saved = (self.item.price - self.item.discount_price) * \
                self.quantity
            return saved
        return saved

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def get_total_seedlings(self):
        total = 0
        if self.item.germination_rate and self.item.seeds_kg:
            number = int(self.item.germination_rate) * \
                int(self.item.seeds_kg) / 100
            total = number * float(self.quantity)
            return total
        return total


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.email

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_total_amount_saved(self):
        amount = 0
        for order_item in self.items.all():
            amount += order_item.get_amount_saved()
            return amount
        return amount

    def subtotal(self):
        return self.get_total() + self.get_total_amount_saved()

    def order_detail_url(self):
        return reverse('store:order-detail', kwargs={'pk': self.id})

    def cancel_url(self):
        return reverse('store:cancel-order', kwargs={'pk': self.id})

    def received_url(self):
        return reverse('store:received-order', kwargs={'pk': self.id})

    def request_refund(self):
        return reverse('store:request-refund', kwargs={'pk': self.id})


class Address(models.Model):
    # CHOICES
    ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
    )
    # DATABASE FIELDS
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=30, blank=True)
    mobile_number = models.CharField(max_length=50, blank=True, null=True)
    secondary_email = models.EmailField(blank=True, unique=False, null=True)
    country = CountryField(multiple=False, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    default = models.BooleanField(default=False)
    address_type = models.CharField(
        max_length=1, choices=ADDRESS_CHOICES, default='S')

    # FUNCTIONS
    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    mobile_number = models.CharField(
        _('mobile number'), max_length=13, blank=True, null=True)

    def __str__(self):
        return self.user.first_name


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
