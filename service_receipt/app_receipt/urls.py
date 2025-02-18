from django.urls import include, path
from rest_framework import routers
from .views import Receipt

router = routers.SimpleRouter()
router.register('', Receipt, basename='receipt')
urlpatterns = [
    path('', include(router.urls)),
]
