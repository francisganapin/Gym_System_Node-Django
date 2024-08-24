from django.urls import path
from .views import registerTrainor_views,loginMember_views,showMember_views,showTrainor_views,registerMember_views,registerClass_views, updateMember_views,deleteMember_views

urlpatterns = [

    path('api/trainor/', showTrainor_views, name='showTrainor_views'),
    path('api/register/trainor', registerTrainor_views, name='registerTrainor_views'),

    path('api/register/member',registerMember_views,name='registerMember_views'),
    path('api/members/', showMember_views, name='show_members'),
    path('api/delete/member',deleteMember_views,name='deleteMember_views'),
    path('api/update/member',updateMember_views,name='updateMember_views'),
    path('api/login/member',loginMember_views,name='loginMember_views'),

    # all about class 
    path('api/register/class',registerClass_views,name='registerClass_views')
]


