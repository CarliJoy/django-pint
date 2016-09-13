from django.test import TestCase

from quantityfield.fields import QuantityField

from quantityfield import ureg
Quantity = ureg.Quantity

from django.db import transaction

from tests.dummyapp.models import HayBale, EmptyHayBale

from pint import DimensionalityError, UndefinedUnitError


class TestFieldCreate(TestCase):

	def test_sets_units(self):
		test_grams = QuantityField('gram')
		self.assertEqual(test_grams.units, ureg.gram)

	def test_fails_with_unknown_units(self):
		with self.assertRaises(ValueError):
			test_crazy_units = QuantityField('zinghie')

	def test_base_units_is_required(self):
		with self.assertRaises(ValueError):
			no_units = QuantityField()

class TestFieldSave(TestCase):

	def setUp(self):
		HayBale.objects.create(weight=100, name="grams")
		HayBale.objects.create(weight=Quantity(10*ureg.ounce), name="ounce")
		self.lightest = HayBale.objects.create(weight=1, name="lightest")
		self.heaviest = HayBale.objects.create(weight=1000, name="heaviest")
		EmptyHayBale.objects.create(name="Empty")

	def test_stores_value_in_base_units(self):
		item = HayBale.objects.get(name='ounce')
		self.assertEqual(item.weight.units, 'gram')
		self.assertAlmostEqual(item.weight.magnitude, 283.49523125)

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

	def test_accepts_null(self):
		empty = EmptyHayBale.objects.first()
		self.assertEqual(empty.weight, None)


	def test_value_stored_as_quantity(self):
		obj = HayBale.objects.first()
		self.assertIsInstance(obj.weight, Quantity)
		self.assertEqual(str(obj.weight), '100.0 gram')

	def test_value_conversion(self):
		obj = HayBale.objects.first()
		ounces = obj.weight.to(ureg.ounce)
		self.assertAlmostEqual(ounces.magnitude, 3.52739619496)
		self.assertEqual(ounces.units, ureg.ounce)

	def test_order_by(self):
		qs = HayBale.objects.all().order_by('weight')
		self.assertEqual(qs[0].name, 'lightest')


	def test_comparison_with_number(self):
		qs = HayBale.objects.filter(weight__gt=2)
		self.assertNotIn(self.lightest, qs)

	def test_comparison_with_quantity(self):
		weight = Quantity(20 * ureg.gram)
		qs = HayBale.objects.filter(weight__gt=weight)
		self.assertNotIn(self.lightest, qs)

	def test_comparison_with_quantity_respects_units(self):
		# 1 ounce = 28.34 grams
		weight = Quantity(0.8 * ureg.ounce)
		qs = HayBale.objects.filter(weight__gt=weight)
		self.assertNotIn(self.lightest, qs)

	def test_comparison_is_actually_numeric(self):
		qs = HayBale.objects.filter(weight__gt=1.0)
		self.assertNotIn(self.lightest, qs)


	def tearDown(self):
		HayBale.objects.all().delete()
		EmptyHayBale.objects.all().delete()




		
		