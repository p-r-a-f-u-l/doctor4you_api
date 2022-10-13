from django.contrib import admin

from .models import FeeModel, AppointmentModel, PatientModel, PatientOptionalData

admin.site.register(FeeModel)
admin.site.register(AppointmentModel)
admin.site.register(PatientModel)
admin.site.register(PatientOptionalData)
