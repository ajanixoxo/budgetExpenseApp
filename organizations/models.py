from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='org_logos/', null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='owned_organizations')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
