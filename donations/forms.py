# donations/forms.py
from django import forms
from .models import Donation
from products.models import Product  # or adjust import as per your app

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['product', 'charity_name']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DonationForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(seller=user)
