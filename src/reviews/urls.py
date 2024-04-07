from rest_framework.routers import DefaultRouter

from reviews.views import AttractionReviewViewSet, TourReviewViewSet

router = DefaultRouter()

router.register('attraction', AttractionReviewViewSet, basename='attr-reviews')
router.register('tour', TourReviewViewSet, basename='tour-reviews')

urlpatterns = router.urls
