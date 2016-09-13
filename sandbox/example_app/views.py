from django.shortcuts import render

from django.views.generic import FormView, TemplateView

from .forms import TestForm

from django.contrib import messages

from quantityfield import ureg

# Create your views here.

class QuantityFormView(TemplateView):
	form_class = TestForm
	template_name = 'test_form.html'

	def get_context_data(self):
		ctx = super(QuantityFormView, self).get_context_data()
		form = TestForm(self.request.GET or None)
		if form.is_valid():
			ctx['value'] = form.cleaned_data['amount'].to('gram')
		ctx['form'] = form
		return ctx


		