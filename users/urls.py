from rest_framework import routers
from .views import MyUserViewSet

router = routers.DefaultRouter()
router.register('users', MyUserViewSet, 'users')
urlpatterns = router.urls