# from django.urls import path

# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
# ]

from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
# router.register(r'working-block', views.WorkingBlockViewSet)
# router.register(r'worker', views.WorkerViewSet)
# router.register(r'job', views.JobViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('email-xlsx/', views.email_xlsx),
    # path('create-xlsx/', views.create_xlxs),
    # path('can-create-xlsx/', views.can_create_xlxs),
    # path('get-relevent-blocks/', views.get_relevent_working_blocks),
    # path('can-access-admin/', views.can_access_admin),
]
