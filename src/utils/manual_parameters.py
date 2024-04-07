from drf_yasg import openapi

QUERY_LATITUDE = openapi.Parameter('lat', openapi.IN_QUERY,
                                   description='current latitude',
                                   required=True,
                                   type=openapi.TYPE_NUMBER)
QUERY_LONGITUDE = openapi.Parameter('lng', openapi.IN_QUERY,
                                    description='current longitude',
                                    required=True,
                                    type=openapi.TYPE_NUMBER)