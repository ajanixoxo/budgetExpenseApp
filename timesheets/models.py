from django.db import models

class Timesheet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    startDate = models.DateField()
    endDate = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='timesheets')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='timesheets')
    hourlyRate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class TimesheetEntry(models.Model):
    description = models.TextField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    duration = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    timesheet = models.ForeignKey('timesheets.Timesheet', on_delete=models.CASCADE, related_name='entries')

    def __str__(self):
        return f"Entry for {self.timesheet.name}"
from django.db import models

# Create your models here.
