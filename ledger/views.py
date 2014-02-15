from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from ledger.models import Expense
from ledger.forms import ExpenseForm

# Create your views here.

def index(request):
   expense_list = Expense.objects.all().order_by('-date')
   template = loader.get_template('ledger/index.html')
   expenseForm = ExpenseForm()
   context = RequestContext(request, {'expense_list': expense_list,'expenseForm': expenseForm})
   return HttpResponse(template.render(context))

def submit(request):
   querydict = request.POST
   expenseType = querydict.get('expenseType')
   date = querydict.get('date')
   amount = querydict.get('amount')
   try:
      Expense.objects.create(expenseType=expenseType,date=date,amount=amount)
   except:
      return HttpResponse("Could not be submitted")
   else:
      return redirect(index)
      

