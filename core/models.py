from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    startDate = models.DateField()
    endDate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='ACTIVE')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
