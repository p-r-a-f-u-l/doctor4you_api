from django.contrib.auth import get_user_model
from django.db import models as model
from django.contrib.gis.db import models

User = get_user_model()


class DoctorSchedule(models.Model):
    day = models.CharField(max_length=10, blank=False)
    start_time = models.TimeField(blank=False)
    stop_time = models.TimeField(blank=False)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.day


class DoctorRating(models.Model):
    feedback = models.TextField(max_length=522, blank=True)
    recom = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=False)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Doctor Feedback"


class DoctorModel(models.Model):
    drImage = models.ImageField(upload_to="media/doctor/", blank=True)
    drName = models.CharField(max_length=120, blank=False)
    location = models.PointField(null=True)
    favourite = models.ManyToManyField(User, related_name="post_favourite", blank=True)
    drSpec = models.CharField(max_length=120, blank=False)
    specIcon = models.ImageField(upload_to="media/doctor/spec/", blank=True)
    drExp = models.IntegerField(blank=False)
    drHospital = models.CharField(max_length=120, blank=False)
    drRating = models.ManyToManyField(DoctorRating, blank=True)
    drAbout = models.TextField(max_length=522, blank=False)
    drAvail = models.ManyToManyField(DoctorSchedule)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.drName

    class Meta:
        verbose_name_plural = "Doctor"
