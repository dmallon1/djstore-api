from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'product-instance', views.ProductInstanceViewSet)
router.register(r'order', views.OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
