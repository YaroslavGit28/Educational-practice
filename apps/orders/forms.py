from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "delivery_address", "phone", "comment")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields["full_name"].required = False
            self.fields["delivery_address"].required = False
            self.fields["phone"].required = False
            self.fields["full_name"].widget = forms.HiddenInput()
            self.fields["delivery_address"].widget = forms.HiddenInput()
            self.fields["phone"].widget = forms.HiddenInput()


class GuestOrderLookupForm(forms.Form):
    order_id = forms.IntegerField(min_value=1, label="Номер заказа")


class OrderContactForm(forms.Form):
    full_name = forms.CharField(max_length=255, label="ФИО")
    phone = forms.CharField(max_length=30, label="Телефон")
    delivery_address = forms.CharField(widget=forms.Textarea, label="Адрес доставки")
