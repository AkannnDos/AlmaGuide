from rest_framework.routers import DefaultRouter

from users.views import SignUpView

router = DefaultRouter()

router.register('auth/sign-up', SignUpView, basename='sign-up')

urlpatterns = router.urls
