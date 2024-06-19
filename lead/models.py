from django.db import models

import uuid

from customer.models import Customer


class Lead(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class WorkerLead(Lead):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='worker_leads')

    def __str__(self):
        return self.name


class EmployeeLead(Lead):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='employee_leads')

    def __str__(self):
        return self.name
