from django import forms
from .models import Message
from products.models import Product

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Only include the content field in the form

    def __init__(self, *args, **kwargs):
        # We expect 'sender' and 'receiver' to be passed, so we set them when initializing the form
        sender = kwargs.pop('sender', None)
        receiver = kwargs.pop('receiver', None)
        product_id = kwargs.pop('product_id', None)  # Optional: get the product if passed

        super().__init__(*args, **kwargs)

        # Set the sender, receiver, and product fields automatically
        if sender:
            self.instance.sender = sender
        if receiver:
            self.instance.receiver = receiver
        if product_id:
            self.instance.product = Product.objects.get(id=product_id) if product_id else None
