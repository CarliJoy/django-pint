
from django import forms

from django_quantityfield.fields import QuantityFormField

class TestForm(forms.Form):
	"""docstring for TestForm"""

	amount = QuantityFormField(units=['ounce', 'gram'])

