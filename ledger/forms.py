from django import forms
from djangular.forms.angular_model import NgModelFormMixin
from ledger.models import Expense, Supplier, Customer

class ExpenseForm(NgModelFormMixin, forms.ModelForm):
   class Meta:
      model = Expense
      fields = ['expenseType','date','amount']
