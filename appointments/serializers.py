from rest_framework import serializers
from .models import PatientOptionalData, PatientModel, FeeModel, AppointmentModel

from doctors.serializers import DoctorSelectSerializer
from doctors.models import DoctorModel


class PatientOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientOptionalData
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    allergy = PatientOptionSerializer()

    class Meta:
        model = PatientModel
        fields = "__all__"

    def create(self, validated_data):
        optionaldata = validated_data.pop("allergy")
        optional_datas = PatientOptionSerializer.create(
            PatientOptionSerializer(), validated_data=optionaldata
        )
        patient_data = PatientModel.objects.create(
            allergy=optional_datas, **validated_data
        )
        return patient_data


class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeModel
        fields = (
            "id",
            "icn",
            "title",
            "hintText",
            "fee",
        )


class AppointmentSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    user = PatientSerializer(read_only=False)
    doctor = serializers.PrimaryKeyRelatedField(queryset=DoctorModel.objects.all())
    feeStructure = serializers.PrimaryKeyRelatedField(
        queryset=FeeModel.objects.all()
    )  # FeeSerializer(many=True)

    class Meta:
        model = AppointmentModel
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        user_data = PatientSerializer.create(PatientSerializer(), validated_data=user)
        appointment = AppointmentModel.objects.create(user=user_data, **validated_data)
        return appointment


class UpcomingSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    user = PatientSerializer(read_only=False)
    doctor = DoctorSelectSerializer()
    feeStructure = FeeSerializer()

    class Meta:
        model = AppointmentModel
        fields = "__all__"


class ShortDetailUpcomingSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    doctor_name = serializers.SerializerMethodField()
    contact_mode = serializers.SerializerMethodField()
    contact_mode_icn = serializers.SerializerMethodField()
    doctor_icn = serializers.SerializerMethodField()
    progrss_status = serializers.SerializerMethodField()

    def get_doctor_name(self, obj: AppointmentModel):
        return obj.doctor.drName

    def get_contact_mode(self, obj: AppointmentModel):
        return obj.feeStructure.title

    def get_contact_mode_icn(self, obj: AppointmentModel):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.feeStructure.icn.url)

    def get_progrss_status(self, obj):
        return "In Progress"

    def get_doctor_icn(self, obj: AppointmentModel):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.doctor.drImage.url)

    class Meta:
        model = AppointmentModel
        fields = (
            "id",
            "owner",
            "doctor_name",
            "contact_mode",
            "contact_mode_icn",
            "doctor_icn",
            "progrss_status",
            "appoint_time",
            "created_at",
            "updated_at",
        )


class SShortDetailUpcomingSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    doctor_name = serializers.SerializerMethodField()
    contact_mode = serializers.SerializerMethodField()
    contact_mode_icn = serializers.SerializerMethodField()
    doctor_icn = serializers.SerializerMethodField()
    progrss_status = serializers.SerializerMethodField()

    def get_doctor_name(self, obj: AppointmentModel):
        return obj.doctor.drName

    def get_contact_mode(self, obj: AppointmentModel):
        return obj.feeStructure.title

    def get_contact_mode_icn(self, obj: AppointmentModel):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.feeStructure.icn.url)

    def get_progrss_status(self, obj):
        return "Finished"

    def get_doctor_icn(self, obj: AppointmentModel):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.doctor.drImage.url)

    class Meta:
        model = AppointmentModel
        fields = (
            "id",
            "owner",
            "doctor_name",
            "contact_mode",
            "contact_mode_icn",
            "doctor_icn",
            "progrss_status",
            "appoint_time",
            "created_at",
            "updated_at",
        )
