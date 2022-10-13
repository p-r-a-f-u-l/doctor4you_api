from django.contrib import admin

from .models import DoctorModel, DoctorRating, DoctorSchedule

admin.site.register(DoctorRating)
admin.site.register(DoctorModel)
admin.site.register(DoctorSchedule)
