from django.http import JsonResponse
from .models import gym_members,gym_trainor,gym_item,gym_classes
from django.core.serializers import serialize
from .forms import RegisterFormMember, RegisterFormClass, RegisterFormTrainor
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
def loginMember_views(request):
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
       
                return JsonResponse({'success': False, 'message': f'Member does not exist'})

            
            # select expiry
            cursor.execute('SELECT expiry FROM gym_members WHERE id_card=%s', [id_card])
            expiry = cursor.fetchone()

            # select expiry result
            expiry_result = expiry[0] if expiry else 'N/A'

            return JsonResponse({'success': True, 'message': f'Member expiry was {expiry_result}'})
        
        except mysql.connector.Error as err:
            return JsonResponse({'success': False, 'message': f'Database error: {err}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    
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


@csrf_exempt
def registerTrainor_views(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
        
        # Initialize the form with parsed JSON data
        form = RegisterFormTrainor(data)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Register Member was Sucessfull successful'})
        else:
            # For debugging: Print form errors
            print("Form validation errors:", form.errors)
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    



@csrf_exempt
def deleteTrainor_views(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                trainor_id = data.get('trainor_id')
                connection = mysql.connector.connect(**config_server)
                cursor = connection.cursor()

                cursor.execute('SELECT COUNT(*) FROM gym_trainor WHERE trainor_id=%s',[trainor_id])
                result = cursor.fetchone()

                if result[0] == 0:
                    return JsonResponse({'success':False,'message':'Trainor does not exist'})
                
                cursor.execute('DELETE FROM gym_trainor WHERE trainor_id=%s',[trainor_id])

                return JsonResponse({'success': True, 'message': 'Trainor deleted successfully'})
        
            except mysql.connector.Error as err:
                return JsonResponse({'success': False, 'message': f'Database error: {err}'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})







def showItem_views(request):
    gym_items_inventory = gym_item.objects.all()

    gym_item_list =[
        {
        'id':gym_items.pk,
        'item_name':gym_items.item_name,
        'stock':gym_items.stock,
        'description':gym_items.description,
        'supplier':gym_items.supplier,
        'phone_number':gym_items.phone_number
        }
        for gym_items in gym_items_inventory
        ]
    response_data  = {
        'success':True,
        'data':gym_item_list
    }
    return JsonResponse(response_data)

@csrf_exempt 
def registerItem_views(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_name = data.get('item_name')
            stock = data.get('stock')
            description = data.get('description')
            supplier = data.get('supplier')
            phone_number = data.get('phone_number')

            
            connection = mysql.connector.connect(**config_server)
            cursor = connection.cursor()

         
            # Proceed with the update if the member exists
            cursor.execute('INSERT INTO gym_item (item_name,stock,description,supplier,phone_number) VALUES(%s,%s,%s,%s,%s)', [item_name,stock,description,supplier,phone_number])
            connection.commit()  # Commit the transaction

            return JsonResponse({'success': True, 'message': f'item was into {item_name} successfully'})
        
        except mysql.connector.Error as err:
            return JsonResponse({'success': False, 'message': f'Database error: {err}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})




@csrf_exempt 
def updateItem_views(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_name = data.get('item_name')
            stock = data.get('stock')
            
            connection = mysql.connector.connect(**config_server)
            cursor = connection.cursor()

            #check if member exist
            cursor.execute('SELECT COUNT(*) FROM gym_item WHERE item_name=%s', [item_name])
            result = cursor.fetchone()

            #if member is not exist say member does not exist3
            if result[0] == 0: 
                return JsonResponse({'success': False, 'message': 'Item does not exist'})

            # Proceed with the update if the member exists
            cursor.execute('UPDATE gym_item SET stock=%s WHERE item_name=%s', [stock, item_name])
            connection.commit()  # Commit the transaction

            return JsonResponse({'success': True, 'message': f'item was into {stock} successfully'})
        
        except mysql.connector.Error as err:
            return JsonResponse({'success': False, 'message': f'Database error: {err}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def deleteItem_views(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_name = data.get('item_name')

            connection = mysql.connector.connect(**config_server)
            cursor = connection.cursor()


            cursor.execute('SELECT COUNT(*) FROM gym_item WHERE item_name=%s', [item_name])
            result = cursor.fetchone()

            #if member is not exist say member does not exist3
            if result[0] == 0: 
                return JsonResponse({'success': False, 'message': 'Item does not exist'})

            # Proceed with the update if the member exists
            cursor.execute('DELETE FROM gym_item  WHERE item_name= %s', [item_name])
            connection.commit()  # Commit the transaction
            return JsonResponse({'success': True, 'message': f'item was delete {item_name} successfully'})
        
        except mysql.connector.Error as err:
            return JsonResponse({'success': False, 'message': f'Database error: {err}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    



def showClass_view(request):
    classes_gym = gym_classes.objects.all()

    gym_classes_list = [
        {
            'id': class_gym.pk,
            'class_name': class_gym.class_name,
            'class_type':class_gym.class_type,
            'class_day': class_gym.class_day,
            'class_hour': class_gym.class_hour,
            'trainor_name': class_gym.trainor_name
        }
        for class_gym in classes_gym
    ]

    response_data = {
        'success': True,
        'data': gym_classes_list
    }

    return JsonResponse(response_data)



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
    



@csrf_exempt
def deleteClass_views(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            class_name = data.get('class_name')

            connection = mysql.connector.connect(**config_server)
            cursor = connection.cursor()

            cursor.execute('SELECT COUNT(*) FROM gym_classes WHERE class_name=%s',[class_name])
            result = cursor.fetchone()

            if result[0] == 0:
                return JsonResponse({'success':False,'message':'Class does not exist'})
            
            cursor.execute('DELETE FROM gym_classes WHERE class_name = %s', (class_name,))

            connection.commit()
            return JsonResponse({'success': True, 'message': f'Class was delete {class_name} successfully'})
        
        except mysql.connector.Error as err:
            return JsonResponse({'success': False, 'message': f'Database error: {err}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    