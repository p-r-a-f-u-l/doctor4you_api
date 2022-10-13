from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from doctors.models import DoctorModel, DoctorRating
from doctors.serializers import DoctorRatingSerializer

from .serializers import (
    PatientSerializer,
    PatientOptionSerializer,
    FeeSerializer,
    AppointmentSerializer,
    ShortDetailUpcomingSerializer,
    UpcomingSerializer,
)
from .models import PatientModel, PatientOptionalData, FeeModel, AppointmentModel


class ResponseInfo(object):
    def __init__(self, **args):
        self.response = {
            "message": args.get("message", "success"),
            "error": args.get(
                "error",
            ),
            "data": args.get("data", []),
        }


class PatientView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(PatientView, self).__init__(**kwargs)

    queryset = PatientModel.objects.all()
    serializer_class = PatientSerializer
    http_method_names = ("get", "post", "put", "delete")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return PatientModel.objects.all()

    def list(self, request, *args, **kwargs):
        response_data = super(PatientView, self).list(request=request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class AppointmentView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(AppointmentView, self).__init__(**kwargs)

    queryset = AppointmentModel.objects.all()
    serializer_class = AppointmentSerializer
    http_method_names = ("get", "post")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        data_context = {
            "data": "Appointment Create Successfully",
            "message": "success",
            "error": None,
        }
        return Response(data=data_context)

    def get_queryset(self):
        return AppointmentModel.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        response_data = super(AppointmentView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class FeeView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(FeeView, self).__init__(**kwargs)

    queryset = FeeModel.objects.all()
    serializer_class = FeeSerializer
    http_method_names = ("get", "post")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return FeeModel.objects.all()

    def list(self, request, *args, **kwargs):
        response_data = super(FeeView, self).list(request=request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class UpcomingAppointView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpcomingAppointView, self).__init__(**kwargs)

    queryset = AppointmentModel.objects.all()
    serializer_class = UpcomingSerializer
    http_method_names = ("get",)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return AppointmentModel.objects.filter(appoint_time__gte=timezone.now())

    def get_serializer_class(self):
        if self.action == "list":
            return ShortDetailUpcomingSerializer
        else:
            return UpcomingSerializer

    def list(self, request, *args, **kwargs):
        response_data = super(UpcomingAppointView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class PastAppointView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(PastAppointView, self).__init__(**kwargs)

    queryset = AppointmentModel.objects.all()
    serializer_class = AppointmentSerializer
    http_method_names = ("get",)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return AppointmentModel.objects.filter(appoint_time__lte=timezone.now())

    def get_serializer_class(self):
        if self.action == "list":
            return SShortDetailUpcomingSerializer
        else:
            return UpcomingSerializer

    def list(self, request, *args, **kwargs):
        response_data = super(PastAppointView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class DoctorReviewView(APIView):
    def get(self, request, pk):
        query = get_object_or_404(AppointmentModel, id=pk)
        print(query.is_reviewed)
        serializer = AppointmentSerializer(query)
        data = {"Info": "ONLY POST METHOD", "status": status.HTTP_204_NO_CONTENT}
        return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk):
        queryset = get_object_or_404(AppointmentModel, id=pk)
        if queryset.is_reviewed:
            data = {
                "status": "failed",
                "message": "Review Aleady Added",
                "error": status.HTTP_409_CONFLICT,
            }
            return Response(data=data, status=status.HTTP_409_CONFLICT)
        serializer = DoctorRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(users=request.user)
        data_id = serializer.data.get("id")
        query = get_object_or_404(DoctorRating, id=data_id)
        doctorQuery = get_object_or_404(DoctorModel, id=pk)
        doctorQuery.drRating.add(query)
        data = {
            "status": "success",
            "message": "Review Added",
            "error": status.HTTP_201_CREATED,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
