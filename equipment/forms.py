from django import forms
from django.utils import timezone

from .models import BorrowRequest, Equipment


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ["name", "category", "description", "quantity_available", "status"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_category(self):
        return self.cleaned_data["category"].strip()


class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ["equipment", "quantity", "purpose", "borrow_date", "return_date"]
        widgets = {
            "borrow_date": forms.DateInput(attrs={"type": "date"}),
            "return_date": forms.DateInput(attrs={"type": "date"}),
            "purpose": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipment"].queryset = Equipment.objects.filter(
            status=Equipment.STATUS_AVAILABLE,
            quantity_available__gt=0,
        )

    def clean_purpose(self):
        purpose = self.cleaned_data["purpose"].strip()
        if not purpose:
            raise forms.ValidationError("Purpose cannot be empty.")
        return purpose

    def clean(self):
        cleaned = super().clean()
        equipment = cleaned.get("equipment")
        quantity = cleaned.get("quantity")
        borrow_date = cleaned.get("borrow_date")
        return_date = cleaned.get("return_date")
        today = timezone.localdate()

        if borrow_date and borrow_date < today:
            self.add_error("borrow_date", "Borrow date cannot be in the past.")
        if borrow_date and return_date and return_date <= borrow_date:
            self.add_error("return_date", "Return date must be after borrow date.")
        if equipment:
            if equipment.status != Equipment.STATUS_AVAILABLE:
                self.add_error("equipment", "This equipment is not available.")
            if quantity and quantity > equipment.quantity_available:
                self.add_error("quantity", "Requested quantity exceeds available quantity.")
        return cleaned
