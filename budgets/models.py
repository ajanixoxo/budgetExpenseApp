from tarfile import NUL
from django.db import models



class Budget(models.Model):
    name= models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    startDate = models.DateField()
    endDate = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    # The organization ForeignKey already links the organization and stores its ID in the database.
    # You do not need a separate organizationId field.
    # To access the organization ID, use budget_instance.organization_id
    
    def __str__(self):
        return self.name
    
class BudgetCategory(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(null=True, blank=True)
    allocatedAmount= models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)
    udpatedAt = models.DateTimeField(auto_now=True)
    budget = models.ForeignKey(
        'budgets.Budget',
        on_delete=models.CASCADE ,
        related_name='categories',
        
    ),
    def __str__(self):
        return self.title
    
       
    