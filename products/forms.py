# products/forms.py
from django import forms
from .models import Product, ProductImage,Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'condition', 
                 'category', 'location', 'main_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.CheckboxSelectMultiple(
                attrs={'class': 'category-checkbox-group'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the queryset is properly set for categories
        self.fields['category'].queryset = Category.objects.all()


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

ProductImageFormSet = forms.inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,  # Shows 3 empty image fields (total 4 with main image)
    min_num=3,
    max_num=3,
    validate_min=True,
    can_delete=False
)

class ProductStatusForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['status']