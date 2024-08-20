from django.urls import path
from .views import showMember_views,showTrainor_views

urlpatterns = [
    path('api/members/', showMember_views, name='show_members'),
    path('api/trainor/', showTrainor_views, name='showTrainor_views'),
]
