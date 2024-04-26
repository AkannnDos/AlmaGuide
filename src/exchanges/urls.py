from rest_framework.routers import DefaultRouter

from exchanges.views import ExchangeRateView

router = DefaultRouter()

router.register('', ExchangeRateView, basename='exchanges')

urlpatterns = router.urls
