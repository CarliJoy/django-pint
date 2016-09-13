from django.test import TestCase

from quantityfield.fields import QuantityField, QuantityFormField
from quantityfield.widgets import QuantityWidget


from quantityfield import ureg
Quantity = ureg.Quantity

from django.db import transaction

from tests.dummyapp.models import HayBale, EmptyHayBale

from django import forms


class HayBaleForm(forms.ModelForm):
	class Meta:
		model = HayBale
		exclude = []
		widgets = {
			'weight':QuantityWidget(base_units='gram', allowed_types=['ounce','gram'])
		}

class NullableWeightForm(forms.Form):
	weight = QuantityFormField(base_units='gram', required=False)


class TestWidgets(TestCase):
	def test_creates_correct_widget_for_modelform(self):
		form = HayBaleForm()
		self.assertIsInstance(form.fields['weight'], QuantityFormField)
		self.assertIsInstance(form.fields['weight'].widget, QuantityWidget)

	def test_displays_initial_data_correctly(self):
		form = HayBaleForm(initial={'weight':Quantity(100 * ureg.gram), 'name':'test'})

	def test_clean_yields_quantity(self):
		form = HayBaleForm(data={'weight_0':100.0, 'weight_1':'gram', 'name':'test'})
		self.assertTrue(form.is_valid())
		self.assertIsInstance(form.cleaned_data['weight'], Quantity)

	def test_clean_yields_quantity_in_correct_units(self):
		form = HayBaleForm(data={'weight_0':1.0, 'weight_1':'ounce', 'name':'test'})
		self.assertTrue(form.is_valid())
		self.assertEqual(str(form.cleaned_data['weight'].units), 'gram')
		self.assertAlmostEqual(form.cleaned_data['weight'].magnitude, 28.349523125)

	def test_base_units_is_required_for_form_field(self):
		with self.assertRaises(ValueError):
			field = QuantityFormField()

	def test_quantityfield_can_be_null(self):
		form = NullableWeightForm(data={'weight_0':None, 'weight_1':None})
		self.assertTrue(form.is_valid())

		
			