from django.http import JsonResponse
from .models import gym_members,gym_trainor
from django.core.serializers import serialize
import json

from datetime import date



class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super(DateEncoder, self).default(obj)

def showMember_views(request):
    members = gym_members.objects.all()

    # Convert QuerySet to list of dictionaries
    member_list = [
        {
            'id': member.pk,
            'id_card': member.id_card,
            'expiry': member.expiry.isoformat() if isinstance(member.expiry, date) else member.expiry,
            'membership': member.membership,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'phone_number': member.phone_number,
            'address': member.address
        }
        for member in members
    ]

    # Construct the response dictionary
    response_data = {
        "success": True,
        "data": member_list
    }

    # Serialize the list to JSON using the DateEncoder
    return JsonResponse(response_data, encoder=DateEncoder)




def showTrainor_views(request):
    trainor = gym_trainor.objects.all()

    trainor_list  =[
        {
            'id':trainor.pk,
            'tranor_id':trainor.trainor_id,
            'first_name':trainor.first_name,
            'last_name':trainor.last_name,
            'specialty':trainor.specialty,
            'phone_number':trainor.phone_number

                            }
        for trainor in trainor
    ]

    response_data =  {
        'success':True,
        "data":trainor_list
    }

    return JsonResponse(response_data)