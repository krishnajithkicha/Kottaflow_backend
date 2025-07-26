from django.urls import path
from .views import junction_status,set_route, get_route, directions_proxy

urlpatterns = [
    path('status/', junction_status),
    path('route/set/', set_route),   # POST
    path('route/get/', get_route), 
    path('api/directions/', directions_proxy)
]
