from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from ledger.models import Expense

# Create your views here.

def index(request):
   expense_list = Expense.objects.all()
   template = loader.get_template('ledger/index.html');
   context = RequestContext(request, {'expense_list': expense_list,})
   return HttpResponse(template.render(context))
