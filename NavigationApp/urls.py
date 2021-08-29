from django.conf.urls import url
from NavigationApp import views


urlpatterns = [
    url(r"^vehicles$", views.vehicleApi),
    url(r"^vehicles/([0-9]+)$", views.vehicleApi),

    url(r"^navigation$", views.NavigationApi),
    url(r"^navigation/([0-9]+)$", views.NavigationApi),

    url(r"^last-points$", views.LastPointsApi),
    url(r"^last-points/([0-9]+)$", views.LastPointsApi),

    url(r"^cache-dates$", views.CacheDates),
    
    url(r"^last-points-cache$", views.LastPointsWithCache),
    url(r"^last-points-cache/([0-9]+)$", views.LastPointsWithCache),
]