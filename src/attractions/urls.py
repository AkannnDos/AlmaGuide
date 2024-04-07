from rest_framework.routers import DefaultRouter

from attractions.views import AttractionViewSet

router = DefaultRouter()

router.register('', AttractionViewSet, basename='attractions')

urlpatterns = router.urls
