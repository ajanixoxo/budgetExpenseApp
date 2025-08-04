# Timesheet and TimesheetEntry Model Explanation

## Timesheet Model

- `class Timesheet(models.Model):`
  Defines a new model called Timesheet, which will create a table in your database for time tracking.

- `name = models.CharField(max_length=255)`
  A short text field for the timesheet’s name (max 255 characters).

- `description = models.TextField(blank=True, null=True)`
  An optional longer text field for describing the timesheet. `blank=True` allows it to be empty in forms, `null=True` allows NULL in the database.

- `startDate = models.DateField()`
  The date when the timesheet period starts.

- `endDate = models.DateField(null=True, blank=True)`
  The date when the timesheet period ends. Optional.

- `createdAt = models.DateTimeField(auto_now_add=True)`
  Automatically set to the current date/time when the timesheet is created.

- `updatedAt = models.DateTimeField(auto_now=True)`
  Automatically updated to the current date/time every time the timesheet is saved.

- `user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='timesheets')`
  Links each timesheet to the user who owns it. `on_delete=models.CASCADE` means if the user is deleted, their timesheets are deleted too. `related_name='timesheets'` lets you access all timesheets for a user with `user.timesheets.all()`.

- `organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='timesheets')`
  Links each timesheet to an organization. Same cascade and reverse lookup logic as above.

- `hourlyRate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)`
  The hourly rate for the timesheet. Optional decimal value.

- `def __str__(self): return self.name`
  Returns the timesheet’s name when you print a Timesheet object or view it in the admin.

## TimesheetEntry Model

- `class TimesheetEntry(models.Model):`
  Defines a new model called TimesheetEntry, which will create a table for individual time entries.

- `description = models.TextField()`
  A text field for describing the work done in this entry.

- `startTime = models.DateTimeField()`
  The date and time when this entry started.

- `endTime = models.DateTimeField()`
  The date and time when this entry ended.

- `duration = models.FloatField()`
  The duration of the entry in hours (or another unit you choose).

- `createdAt = models.DateTimeField(auto_now_add=True)`
  Automatically set to the current date/time when the entry is created.

- `updatedAt = models.DateTimeField(auto_now=True)`
  Automatically updated to the current date/time every time the entry is saved.

- `timesheet = models.ForeignKey('timesheets.Timesheet', on_delete=models.CASCADE, related_name='entries')`
  Links each entry to its parent timesheet. If the timesheet is deleted, its entries are deleted too. `related_name='entries'` lets you access all entries for a timesheet with `timesheet.entries.all()`.

- `def __str__(self): return f"Entry for {self.timesheet.name}"`
  Returns a string showing which timesheet this entry belongs to.
