from django.urls import path
from . import views
urlpatterns = [
    path('trip_form/',views.trip_form),
    path('directions/<str:frm_add>/<str:t_add>',views.directions),
    path('area_type/',views.area_type)
]
