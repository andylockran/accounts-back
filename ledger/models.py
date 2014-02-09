from django.db import models
from django.contrib import admin
from django_fsm.db.fields import FSMField, transition


# Create your models here.

class ExpenseManager(models.Manager):
   "Manager for the Expenses Table"
   def status_count(self, keyword):
      return self.filter(state__icontains=keyword.count())

class Expense(models.Model):
    "This model handles each of the potential expense lines in an invoice."
    EXPENSE_TYPES = (
        ('BANK', 'BANK'),
        ('CASH', 'CASH'),
    )
    
    #Field Definitions
    expenseType = models.CharField(null=False,blank=False,max_length=4,choices=EXPENSE_TYPES)
    date = models.DateField(null=False, blank=False)
    amount = models.DecimalField(null=False,blank=False,decimal_places=2,max_digits=10)
    supplierCode = models.ForeignKey('Supplier', null=True, blank=True,max_length="40")
    nominalCode = models.CharField(null=True, blank=True,max_length="40")
    invoiceRef = models.CharField(null=True, blank=True,max_length="40")
    VATrate = models.CharField(null=True, blank=True,max_length="40")
    VAT = models.IntegerField(null=True, blank=True,max_length="40")
    EU = models.CharField(null=True, blank=True,max_length="40")
    toBeClaimedExpense = models.NullBooleanField(null=True, blank=True)
    state = FSMField(default="none",protected=True)
    objects = ExpenseManager()

    def __unicode__(self):
        return str(self.id)

    def can_post(self):
        if self.supplierCode is None:
             return False
        if self.nominalCode is None:
             return False
        if self.invoiceRef is None:
             return False
        if self.VATrate is None:
             return False
        if self.VAT is None:
             return False
        if self.EU is None:
             return False
        if self.toBeClaimedExpense != 'Yes':
             return False
        return True 

    def has_min(self):
        if self.expenseType is None:
            return False
        if self.date is None:
            return False
        if self.amount is None:
            return False
        return True

    @transition(source="min",target="posted", conditions=[can_post])
    def post(self):
       pass
    
    @transition(source="none",target="min",conditions=[has_min])
    def save(self, *args, **kwargs):
       super(Expense,self).save(*args, **kwargs)

class Supplier(models.Model):
    name = models.CharField(max_length="255")
    code = models.CharField(max_length="8")

    def __unicode__(self):
        return self.code

class Mileage(models.Model):
   date = models.DateField(null=False,blank=False)
   miles = models.IntegerField(null=True,blank=True)
   fromLocation = models.CharField(max_length=40)
   toLocation = models.CharField(max_length=40)
   customer = models.ForeignKey('Customer',blank=True,null=True)
   reason = models.TextField(max_length="1000")
   notes = models.TextField(max_length="1000")
   toBeClaimedExpense = models.NullBooleanField(null=True, blank=True)

   def __unicode__(self):
      return str(self.id)

class RecordSalesInvoice(models.Model):
   invoiceReference = models.CharField(max_length="40")
   date = models.DateField()
   customer = models.ForeignKey('Customer')
   amount = models.DecimalField(null=False,blank=False,decimal_places=2,max_digits=10)
   dueDate = models.DateField(blank=True,null=True)
   paid = models.BooleanField()
   #linkTo = @TODO
   def __unicode__(self):
      return str(self.id)

class RecordSupplierInvoice(models.Model):
   orderReference = models.CharField(max_length="255")
   invoiceReference = models.CharField(max_length="40")
   date = models.DateField()
   customer = models.ForeignKey('Customer')
   amount = models.DecimalField(null=False,blank=False,decimal_places=2,max_digits=10)
   dueDate = models.DateField(blank=True,null=True)
   paid = models.BooleanField()
   #linkTo = @TODO
   def __unicode__(self):
      return str(self.id)

class Customer(models.Model):
   name = models.CharField(max_length="255")
   code = models.CharField(max_length="8")
   def __unicode__(self):
      return self.code


class ExpenseAdmin(admin.ModelAdmin):
   fieldsets = [
         (None, {'fields': ['expenseType','date','amount']}),
         ("Required for POST", {'fields': ['supplierCode','nominalCode','invoiceRef','VATrate','VAT','EU','toBeClaimedExpense']}),
         ("ReadOnly", {'fields': ['state']}),
         ]
   readonly_fields = ('state',)
   list_display = ('amount','date','expenseType','id')


admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Mileage)
admin.site.register(RecordSalesInvoice)
admin.site.register(RecordSupplierInvoice)
