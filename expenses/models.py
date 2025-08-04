from django.db import models

class Expense(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='expenses')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='expenses')
    budget = models.ForeignKey('budgets.Budget', on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey('budgets.BudgetCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title
from django.db import models

# Create your models here.
