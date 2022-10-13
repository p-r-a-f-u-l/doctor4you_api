from rest_framework import serializers

from .models import DoctorModel, DoctorRating, DoctorSchedule


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = (
            "day",
            "start_time",
            "stop_time",
            "available",
            "created_at",
            "updated_at",
        )


class DoctorRatingSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DoctorRating
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    # drRating = DoctorRatingSerializer(many=True)
    drAvail = DoctorScheduleSerializer(many=True)
    favourite = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    customers = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    def get_patient(self, doctor):
        return 100

    def get_favourite(self, doctor):
        request = self.context.get("request")
        if doctor.favourite.filter(id=request.user.id).exists():
            return True
        return False

    def get_rating(self, doctor):
        try:
            avg_rating = sum(i.rating for i in doctor.drRating.all()) / len(
                [i.rating for i in doctor.drRating.all()]
            )
            return float(str(avg_rating)[:3])
        except ZeroDivisionError:
            return 0

    def get_customers(self, doctor):
        return len([i.rating for i in doctor.drRating.all()])

    class Meta:
        model = DoctorModel
        fields = (
            "id",
            "drImage",
            "drName",
            "patient",
            "rating",
            "customers",
            "drSpec",
            "drExp",
            "drHospital",
            "drAbout",
            "drAvail",
            "favourite",
            "created_at",
            "updated_at",
        )


class DoctorCatSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, doctor):
        return DoctorModel.objects.filter(drSpec=doctor.drSpec).count()

    class Meta:
        model = DoctorModel
        fields = (
            "specIcon",
            "drSpec",
            "count",
        )


class DoctorSelectSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    customers = serializers.SerializerMethodField()

    def get_rating(self, doctor):
        try:
            avg_rating = sum(i.rating for i in doctor.drRating.all()) / len(
                [i.rating for i in doctor.drRating.all()]
            )
            return float(str(avg_rating)[:3])
        except ZeroDivisionError:
            return 0

    def get_customers(self, doctor):
        return len([i.rating for i in doctor.drRating.all()])

    class Meta:
        model = DoctorModel
        fields = (
            "id",
            "drImage",
            "drName",
            "rating",
            "customers",
            "drSpec",
            "drHospital",
            "created_at",
            "updated_at",
        )
