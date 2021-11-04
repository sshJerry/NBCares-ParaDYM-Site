from django.db import models

# Create your models here.
EVENT_TAGS = (
    ('None', 'None'),
    ('Toddler', 'Toddler'),
    ('Child', 'Child'),
    ('Adolescent', 'Adolescent'),
    ('Adult', 'Adult'),
    ('Elderly', 'Elderly'),
    ('Other', 'Other'),
)


class ProjectSite(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.CharField(max_length=8)
    event_sTime = models.CharField(max_length=10)
    event_eTime = models.CharField(max_length=10)
    event_description = models.CharField(max_length=400)
    event_tag = models.CharField(max_length=20, blank=True, choices=EVENT_TAGS)

    def __str__(self):
        return self.event_description
