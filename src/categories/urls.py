from rest_framework.routers import DefaultRouter

from categories.views import SubcategoryListView

router = DefaultRouter()

router.register('subcategories', SubcategoryListView, basename='subcategories')

urlpatterns = router.urls
