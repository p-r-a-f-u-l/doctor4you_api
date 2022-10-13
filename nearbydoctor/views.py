from django.views import generic
from django.contrib.gis.geos import fromstr
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance
from .models import Shop
from rest_framework.serializers import ModelSerializer
from django.contrib.gis.geos import Point

from django.contrib.gis.measure import D
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F

longitude = 72.63427912177863
latitude = 22.91522513644759

user_location = Point(longitude, latitude, srid=4326)


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class Home(APIView):
    def get(self, request):
        radius = 500
        # user_location = fromstr("POINT(%s %s)" % (longitude, latitude))
        desired_radius = {"m": radius}
        nearby_spots = (
            Shop.objects.annotate(distance=Distance("location", user_location))
            .order_by("distance")
            .filter(location__distance_lte=(user_location, 7000))
        )
        print(nearby_spots.values_list())
        print(desired_radius)

        # queryset = Shop.objects.filter(
        #     distance=Distance("location", user_location)
        # ).order_by("distance")
        serializer = LocationSerializer(nearby_spots, many=True)
        return Response(data=serializer.data)
