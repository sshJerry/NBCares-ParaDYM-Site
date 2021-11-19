from django.db import models


# Create your models here.


class Organization(models.Model):
    ORGANIZATION_STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    org_name = models.CharField(max_length=40, null=True, blank=False)
    org_address = models.CharField(max_length=60, null=True, blank=True)
    org_phone = models.CharField(max_length=20, null=True, blank=True)
    org_email = models.EmailField(null=True, blank=True)
    org_status = models.CharField(max_length=20, null=True, choices=ORGANIZATION_STATUS)
    org_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.org_name


class Tag(models.Model):
    EVENT_TAGS = (
        ('None', 'None'),
        ('Toddler', 'Toddler'),
        ('Child', 'Child'),
        ('Adolescent', 'Adolescent'),
        ('Adult', 'Adult'),
        ('Elderly', 'Elderly'),
        ('Other', 'Other'),
    )
    tag_name = models.CharField(max_length=30, null=True, blank=True, choices=EVENT_TAGS)

    def __str__(self):
        return self.tag_name


class Event(models.Model):
    # When writing {{ event }}, The description is whats returned
    event_name = models.CharField(max_length=100, null=True, blank=False)
    event_sTime = models.DateTimeField(null=True, blank=False)
    event_eTime = models.DateTimeField(null=True, blank=False)
    event_description = models.CharField(max_length=400, null=True, blank=True)
    # event_tag = models.CharField(max_length=20, blank=True, choices=EVENT_TAGS) PREVIOUS
    # org_event_tag = models.ManyToManyField(Tag)
    event_tag = models.ManyToManyField(Tag, blank=True)
    event_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.event_name


class OrgEvent(models.Model):
    EVENT_STATUS = (
        ('Accepted', 'Accepted'),
        ('Waiting Approval', 'Waiting Approval'),
        # ('Canceled', 'Canceled'),
        # ('Requested For Change', 'Requested For Change'),
    )
    org_event_organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL)
    org_event_event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    org_event_status = models.CharField(max_length=20, null=True, choices=EVENT_STATUS)
    org_event_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.org_event_event.event_name)
    # return str(self.org_event_organization) + " | " + str(self.org_event_event) + " | " + self.org_event_status
