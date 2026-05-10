from django.urls import path
from . import views
from .views import (ComplaintListCreateAPI, ComplaintDetailAPI, DistrictListAPI, MunicipalityListAPI, WardListAPI, ProvinceListAPI, upvote_api, stats_api)

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('upvote/<int:complaint_id>/', views.upvote_complaint, name='upvote_complaint'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('map/', views.map_view, name='map'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/map-data/', views.complaints_map_data, name='complaints_map_data'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/<int:complaint_id>/edit/', views.edit_complaint, name='edit_complaint'),
    path('complaint/<int:complaint_id>/delete/', views.delete_complaint, name='delete_complaint'),
    path('api/districts/', views.get_districts, name='get_districts'),
    path('api/municipalities/', views.get_municipalities, name='get_municipalities'),
    path('api/wards/', views.get_wards, name='get_wards'),
    path('api/complaints/', ComplaintListCreateAPI.as_view(), name='api_complaints'),
    path('api/complaints/<int:pk>/', ComplaintDetailAPI.as_view(), name='api_complaint_detail'),
    path('api/complaints/<int:pk>/upvote/', upvote_api, name='api_upvote'),
    path('api/provinces/', ProvinceListAPI.as_view(), name='api_provinces'),
    path('api/districts/', DistrictListAPI.as_view(), name='api_districts'),
    path('api/municipalities/', MunicipalityListAPI.as_view(), name='api_municipalities'),
    path('api/wards/', WardListAPI.as_view(), name='api_wards'),
    path('api/stats/', stats_api, name='api_stats'),
    path('profile/', views.profile, name='profile'),
]