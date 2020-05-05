from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import SeedProduct
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('M', 'MoMo Pay')
)


class CheckoutForm(forms.Form):
    # SHIPPING ADDRESS
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    shipping_street_address = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_district = forms.CharField(required=False)
    mobile_number = forms.CharField(max_length=100, required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False, widget=CountrySelectWidget(attrs={
            'class': 'custom-select my-1 width-90', }))
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    same_as_billing = forms.BooleanField(required=False)

    # BILLING ADDRESS
    billing_city = forms.CharField(required=False)
    billing_district = forms.CharField(required=False)
    billing_street_address = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    # PAYMENT OPTION
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


    
    
class AddProductForm(forms.ModelForm):
    class Meta:
        model = SeedProduct
        fields = ('__all__')
