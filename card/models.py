from django.db import models


class PartnerType(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PartnerStatus(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Partner(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(PartnerType, on_delete=models.CASCADE)
    status = models.ForeignKey(PartnerStatus, on_delete=models.CASCADE)
    manager = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
