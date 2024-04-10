from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet, SubcategoryListView

router = DefaultRouter()

router.register('subcategories', SubcategoryListView, basename='subcategories')
router.register('', CategoryViewSet, basename='categories')

urlpatterns = router.urls
