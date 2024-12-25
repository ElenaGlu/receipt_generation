from rest_framework import routers

from .views import Receipt

router = routers.SimpleRouter()
router.register(r'receipt', Receipt, basename='receipt')
urlpatterns = router.urls
