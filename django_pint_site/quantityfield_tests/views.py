from django.shortcuts import render

from django.views.generic import FormView

from .forms import TestForm

from django.contrib import messages

from django_quantityfield import ureg

# Create your views here.


class QuantityFormView(FormView):
	form_class = TestForm
	template_name = 'test_form.html'

	success_url = '/'

	result = "fdsfdsf"

	def form_valid(self, form):
		self.result = "Hello"

		amount = form.cleaned_data['amount']

		print amount

		print "In Grams : %s" % ( amount.to(ureg.gram) )
		return super(QuantityFormView, self).form_valid(form)

	def form_invalid(self, form):
		print form.errors
		return super(QuantityFormView, self).form_invalid(form)

	def get_context_data(self):
		context = super(QuantityFormView, self).get_context_data()
		if self.result:
			context['result'] = self.result
		return context

		