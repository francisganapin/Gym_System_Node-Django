from django.urls import path
from .views import showMember_views,showTrainor_views,registerMember_views,registerClass_views

urlpatterns = [
    path('api/members/', showMember_views, name='show_members'),
    path('api/trainor/', showTrainor_views, name='showTrainor_views'),
    path('api/register/member',registerMember_views,name='registerMember_views'),
    path('api/register/class',registerClass_views,name='registerClass_views')
]
