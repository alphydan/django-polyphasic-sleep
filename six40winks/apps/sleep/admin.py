from django.contrib import admin

from sleep.models import SleepPhase, SleepDay

admin.site.register(SleepPhase)
admin.site.register(SleepDay)