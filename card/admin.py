from django.contrib import admin

from .models import Partner, PartnerType, PartnerStatus


admin.site.register(Partner)
admin.site.register(PartnerType)
admin.site.register(PartnerStatus)