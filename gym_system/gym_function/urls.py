from django.urls import path
from .views import deleteClass_views,deleteTrainor_views,showClass_view,showItem_views,registerItem_views,deleteItem_views,updateItem_views,registerTrainor_views,loginMember_views,showMember_views,showTrainor_views,registerMember_views,registerClass_views, updateMember_views,deleteMember_views

urlpatterns = [
            #member
    path('api/register/member',registerMember_views,name='registerMember_views'),
    path('api/members/', showMember_views, name='show_members'),
    path('api/delete/member',deleteMember_views,name='deleteMember_views'),
    path('api/update/member',updateMember_views,name='updateMember_views'),
    path('api/login/member',loginMember_views,name='loginMember_views'),





    path('api/trainor/', showTrainor_views, name='showTrainor_views'),
    path('api/register/trainor', registerTrainor_views, name='registerTrainor_views'),
    path('api/trainor/delete',deleteTrainor_views,name='deleteTrainor_views'),

    #
    path('api/inventory/show',showItem_views,name='showItem_views'),
    path('api/inventory/update',updateItem_views,name='updateItem_views'),
    path('api/inventory/delete',deleteItem_views,name='deleteItem_views'),
    path('api/inventory/insert',registerItem_views,name='registerItem_views'),

    # all about class 
    path('api/show/class',showClass_view,name='showClass_view'),
    path('api/register/class',registerClass_views,name='registerClass_views'),
    path('api/delete/class',deleteClass_views,name='deleteClass_views')
]


