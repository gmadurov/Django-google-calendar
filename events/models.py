from django.db import models

# Create your models here.

# Changed 
class Event(models.Model):
    id: int
    start_date: models.DateField = models.DateField()
    start_time: models.TimeField = models.TimeField(null=True, blank=True)
    end_date: models.DateField = models.DateField(null=True, blank=True)
    end_time: models.TimeField = models.TimeField(null=True, blank=True)

    summary: models.CharField = models.CharField(max_length=50)
    description: models.CharField = models.CharField(
        max_length=50, null=True, blank=True
    )

    # recuring = models.CharField(max_length=50, null=True, blank=True)
    location: models.CharField = models.CharField(max_length=50, null=True, blank=True)
    info: models.TextField = models.TextField(null=True, blank=True)
    google_link: models.CharField = models.CharField(
        max_length=150, null=True, blank=True
    )

    def __str__(self):
        return str(self.description) + ", " + str(self.start_date)

    class Meta:
        ordering = ["start_date", "start_time", "-end_date"]
