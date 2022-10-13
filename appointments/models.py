from django.db import models
from doctors.models import DoctorModel
from django.contrib.auth import get_user_model

User = get_user_model()

g = (
    ("Male", "M"),
    ("Female", "F"),
    ("Other", "O"),
)


class PatientOptionalData(models.Model):
    allergies = models.BooleanField(default=False)
    title = models.CharField(max_length=120, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Patient Sickness"


class PatientModel(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    age = models.IntegerField(default=10, blank=True, null=True)
    contact = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=g, default="M", blank=True, null=True)
    symptoms = models.TextField(max_length=533, blank=True, null=True)
    symptoms_time = models.CharField(blank=True, null=True, max_length=225)
    medication = models.BooleanField(default=False)
    allergy = models.ForeignKey(PatientOptionalData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Patients"


class FeeModel(models.Model):
    icn = models.ImageField(upload_to="media/fee/icon/")
    title = models.CharField(max_length=40, blank=False)
    hintText = models.CharField(max_length=120, blank=False)
    fee = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.fee)

    class Meta:
        verbose_name_plural = "Fee"


class AppointmentModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(PatientModel, on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    appoint_time = models.DateTimeField()
    feeStructure = models.ForeignKey(FeeModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.appoint_time)

    class Meta:
        verbose_name_plural = "Appointment"
