from django.test import TestCase

from quantityfield.fields import QuantityField
from quantityfield import ureg
Quantity = ureg.Quantity

from django.db import transaction

from tests.dummyapp.models import HayBale

from pint import DimensionalityError


class TestFieldCreate(TestCase):

	def test_sets_units(self):
		test_grams = QuantityField('gram')
		self.assertEqual(test_grams.units, ureg.gram)

	def test_fails_with_unknown_units(self):
		with self.assertRaises(ValueError):
			test_crazy_units = QuantityField('zinghie')

class TestFieldSave(TestCase):

	def setUp(self):
		HayBale.objects.create(weight=100, name="grams")
		HayBale.objects.create(weight=Quantity(10*ureg.ounce), name="ounce")

	def test_stores_value_in_base_units(self):
		item = HayBale.objects.get(name='ounce')
		self.assertEqual(item.weight.units, 'gram')
		self.assertEqual(item.weight.magnitude, 283)

	def test_fails_with_incompatible_units(self):
		# we have to wrap this in a transaction 
		# fixing a unit test problem
		# http://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
		metres = Quantity(100 * ureg.meter)
		try:
			with transaction.atomic():
				HayBale.objects.create(weight=metres, name="Should Fail")
			self.assertTrue(0, 'Was able to create weight with metres')
		except DimensionalityError:
			pass
			


	def test_value_stored_as_quantity(self):
		obj = HayBale.objects.first()
		self.assertIsInstance(obj.weight, Quantity)
		self.assertEqual(str(obj.weight), '100 gram')

	def test_value_conversion(self):
		obj = HayBale.objects.first()
		ounces = obj.weight.to(ureg.ounce)
		self.assertAlmostEqual(ounces.magnitude, 3.52739619496)
		self.assertEqual(ounces.units, ureg.ounce)

	def tearDown(self):

		HayBale.objects.all().delete()




		
		