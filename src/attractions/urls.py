from rest_framework.routers import DefaultRouter

from attractions.views import AttractionViewSet, FavouriteViewSet, RouteViewSet

router = DefaultRouter()

router.register('routes', RouteViewSet, basename='routes')
router.register('favourite', FavouriteViewSet, basename='favourite')
router.register('', AttractionViewSet, basename='attractions')

urlpatterns = router.urls
