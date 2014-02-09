from django.test import TestCase
from ledger.models import Expense,Customer,Supplier
from datetime import datetime
# Create your tests here.

class CustomerTestCase(TestCase):
   def setUp(self):
      Customer.objects.create(name="Andy",code="APL")
   def test_customer_by_code(self):
      andy = Customer.objects.get(name="Andy")
      self.assertEqual(andy.name, 'Andy')
      self.assertEqual(andy.code, 'APL')
   def test_can_create_customer_without_code(self):
      karly = Customer.objects.create(name='Karly')
      self.assertEqual(karly.code, "")

class SupplierTestCase(TestCase):
   def setUp(self):
      Supplier.objects.create(name="Des Gregory",code="DG")
   def test_customer_by_code(self):
      des = Supplier.objects.get(name="Des Gregory")
      self.assertEqual(des.name, 'Des Gregory')
      self.assertEqual(des.code, 'DG')
   def test_can_create_customer_without_code(self):
      alex = Supplier.objects.create(name='Alex')
      self.assertEqual(alex.code, "")

class ExpenseTestCase(TestCase):
   def setUp(self):
      Expense.objects.create(expenseType="BANK",date=datetime.today().date(), amount="24.44")
   def test_minimum_info_inputted(self):
      "Test to make sure minimum inputted data is allowed"
      min = Expense.objects.get(amount="24.44")
      self.assertEqual(min.expenseType, "BANK")

