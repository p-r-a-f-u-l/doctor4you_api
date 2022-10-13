from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from doctor4you.customresponse import ResponseInfo
from .models import DoctorModel, DoctorRating
from .serializers import (
    DoctorSelectSerializer,
    DoctorSerializer,
    DoctorCatSerializer,
    DoctorRatingSerializer,
)


class FavIndexID(APIView):
    def get(self, request):
        post = DoctorModel.objects.all(favourite=request.user.id)
        serializer = DoctorSerializer(post, context={"request": request}, many=True)
        data = {
            "message": "success",
            "error": None,
            "data": serializer.data,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class DoctorIndexID(APIView):
    bad_request_message = "An error has occurred"

    def get(self, request, pk):
        post = get_object_or_404(DoctorModel, id=pk)
        serializer = DoctorSerializer(post, context={"request": request})
        data = {
            "message": "success",
            "error": None,
            "data": serializer.data,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = get_object_or_404(DoctorModel, pk=pk)
        if not post.favourite.filter(id=request.user.id).exists():
            post.favourite.add(request.user)
            # DoctorModel.objects.filter(pk=pk).update(is_fav=True)
            return Response({"msg": "Favorite Added."}, status=status.HTTP_200_OK)
        return Response(
            {"msg": "You can't Favorite One Doctor Twice a Time"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        post = get_object_or_404(DoctorModel, pk=pk)
        if post.favourite.filter(id=request.user.id).exists():
            post.favourite.remove(request.user)
            # Product.objects.filter().update(is_fav=False)
            return Response(
                {"msg": "No Longer Favorite."}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"msg": self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST
        )


class DoctorIndex(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DoctorIndex, self).__init__(**kwargs)

    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSelectSerializer
    http_method_names = ("get",)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ("drSpec", "drName")
    ordering_fields = ["drRating__rating"]

    def list(self, request, *args, **kwargs):
        response_data = super(DoctorIndex, self).list(request=request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class DoctorNearByIndex(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DoctorNearByIndex, self).__init__(**kwargs)

    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSelectSerializer
    http_method_names = ("get",)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ("drSpec", "drName")
    ordering_fields = ["drRating__rating"]

    def list(self, request, *args, **kwargs):
        response_data = super(DoctorNearByIndex, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class TopDoctorView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(TopDoctorView, self).__init__(**kwargs)

    queryset = DoctorModel.objects.annotate(rating=Sum("drRating__rating"))
    serializer_class = DoctorSelectSerializer
    http_method_names = ("get",)
    filter_backends = [OrderingFilter]
    ordering_fields = ["rating"]

    def list(self, request, *args, **kwargs):
        response_data = super(TopDoctorView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class DoctorListView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DoctorListView, self).__init__(**kwargs)

    queryset = DoctorModel.objects.all().distinct("drSpec")
    serializer_class = DoctorCatSerializer
    http_method_names = ("get",)

    def list(self, request, *args, **kwargs):
        response_data = super(DoctorListView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class DoctorRateView(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DoctorRateView, self).__init__(**kwargs)

    queryset = DoctorRating.objects.all()
    serializer_class = DoctorRatingSerializer
    http_method_names = ("get", "post")

    def perform_create(self, serializer):
        return serializer.save(users=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        serializer = DoctorRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(users=self.request.user)
            modify = {
                "responseCode": 200,
                "responseStatus": "success",
                "responseError": None,
            }
            return Response(data=modify)
        modify = {
            "responseCode": status.HTTP_400_BAD_REQUEST,
            "responseStatus": "failed",
            "responseError": status.HTTP_400_BAD_REQUEST,
        }
        return Response(data=modify)

    def get_queryset(self):
        return DoctorRating.objects.filter(users=self.request.user)

    def list(self, request, *args, **kwargs):
        response_data = super(DoctorRateView, self).list(
            request=request, *args, **kwargs
        )
        self.response_format["data"] = response_data.data
        if not response_data.data:
            self.response_format["message"] = "NO data found"
            self.response_format["error"] = response_data.status_code
        return Response(self.response_format)


class DoctorAddRate(APIView):
    def get(self, request, pk):
        data = {"status": "ONLY POST METHOD"}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk):
        id = request.data["review"]
        query = get_object_or_404(DoctorRating, id=id)
        doctorQuery = get_object_or_404(DoctorModel, id=pk)
        doctorQuery.drRating.add(query)
        data = {"status": "Review Added"}
        return Response(data=data, status=status.HTTP_201_CREATED)
