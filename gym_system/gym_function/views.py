from django.http import JsonResponse
from .models import gym_members,gym_trainor
from django.core.serializers import serialize
from .forms import RegisterFormMember,RegisterFormClass
import json
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
from datetime import date



#this will config to our server 
config_server = {
    'host':"localhost",  
    'user':'root',  
    'password':'root', 
    'database':'memberdb'
}

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super(DateEncoder, self).default(obj)



@csrf_exempt
def registerMember_views(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
        
        # Initialize the form with parsed JSON data
        form = RegisterFormMember(data)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Register member successful'})
        else:
            # For debugging: Print form errors
            print("Form validation errors:", form.errors)
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt 
def updateMember_views(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_card = data.get('id_card')
            expiry = data.get('expiry')
            
            connection = mysql.connector.connect(**config_server)
            cursor = connection.cursor()

            #check if member exist
            cursor.execute('SELECT COUNT(*) FROM gym_members WHERE id_card=%s', [id_card])
            result = cursor.fetchone()

            #if member is not exist say member does not exist
            if result[0] == 0: 
                return JsonResponse({'success': False, 'message': 'Member does not exist'})

            # Proceed with the update if the member exists
            cursor.execute('UPDATE gym_members SET expiry=%s WHERE id_card=%s', [expiry, id_card])
            connection.commit()  # Commit the transaction

            return JsonResponse({'success': True, 'message': 'Member updated successfully'})
        
        except mysql.connector.Error as err:
            return JsonResponse({'success': False, 'message': f'Database error: {err}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt 
def deleteMember_views(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_card = data.get('id_card')
            connection = mysql.connector.connect(**config_server)
            cursor = connection.cursor()


            cursor.execute('SELECT COUNT(*) FROM gym_members WHERE id_card=%s', [id_card])
            result = cursor.fetchone()

            #if member is not exist say member does not exist
            if result[0] == 0: 
                return JsonResponse({'success': False, 'message': 'Member does not exist'})

            
            # Delete the member
            cursor.execute('DELETE FROM gym_members WHERE id_card=%s', [id_card])

            connection.commit()  # Commit the transaction

            return JsonResponse({'success': True, 'message': 'Member deleted successfully'})
        
        except mysql.connector.Error as err:
            return JsonResponse({'success': False, 'message': f'Database error: {err}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})





@csrf_exempt
def registerClass_views(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
        
        # Initialize the form with parsed JSON data
        form = RegisterFormClass(data)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Register class successful'})
        else:
            # For debugging: Print form errors
            print("Form validation errors:", form.errors)
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


            








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
            'trainor_id':trainor.trainor_id,
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