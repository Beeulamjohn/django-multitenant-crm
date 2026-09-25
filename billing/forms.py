from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = [
            "student",
            "receipt_number",
            "amount",
            "payment_method",
            "payment_date",
            "status",
            "remarks",
        ]