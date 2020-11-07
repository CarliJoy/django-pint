from django.contrib import admin
from .models import Megalith
from django import forms
from quantityfield.fields import QuantityFormField

# Register your models here.


class MegalithForm(forms.ModelForm):

    weight = QuantityFormField(
        base_units="tonnes", unit_choices=["tonnes", "ounces", "grams", "kilograms"]
    )

    class Meta:
        model = Megalith
        fields = "__all__"


class MegalithAdmin(admin.ModelAdmin):
    form = MegalithForm


admin.site.register(Megalith, MegalithAdmin)
