from rest_framework.routers import DefaultRouter

from users.views import SignUpView, ProfileView

router = DefaultRouter()

router.register('auth/sign-up', SignUpView, basename='sign-up')
router.register('users', ProfileView, basename='users')

urlpatterns = router.urls
