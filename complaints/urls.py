from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('upvote/<int:complaint_id>/', views.upvote_complaint, name='upvote_complaint'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('map/', views.map_view, name='map'),
    path('api/map-data/', views.complaints_map_data, name='complaints_map_data'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
]