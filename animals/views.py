from django.http import JsonResponse
from animals.models import Animal
from django.views.decorators.csrf import csrf_exempt
from .models import Animal
import json

@csrf_exempt
def animal_view(request):
    if request.method == 'GET':
        animals = Animal.objects.all()
        animal_list = list(animals.values())  # Converte QuerySet para uma lista de dicionários
        return JsonResponse(animal_list, safe=False)




@csrf_exempt
def animal_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            animal = Animal.objects.create(
                tutor=data['tutor'],
                name=data['name'],
                specie=data['specie'],
                breed=data['breed'],
                service=data['service']
            )
            # Serialize the created animal object to JSON
            serialized_animal = {
                'id': animal.id,
                'tutor': animal.tutor,
                'name': animal.name,
                'specie': animal.specie,
                'breed': animal.breed,
                'service': animal.service
            }
            return JsonResponse({'success': True, 'animal': serialized_animal}, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


        




@csrf_exempt
def animal_update(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            animal_id = data.get('id')
            if animal_id is None:
                return JsonResponse({'error': 'Animal ID not provided in the request body'}, status=400)
            
            animal = Animal.objects.get(id=animal_id)
            animal.tutor = data.get('tutor', animal.tutor)
            animal.name = data.get('name', animal.name)
            animal.specie = data.get('specie', animal.specie)
            animal.breed = data.get('breed', animal.breed)
            animal.service = data.get('service', animal.service)
            animal.save()

            serialized_animal = {
                'id': animal.id,
                'tutor': animal.tutor,
                'name': animal.name,
                'specie': animal.specie,
                'breed': animal.breed,
                'service': animal.service
            }
            return JsonResponse({'success': True, 'animal': serialized_animal})
        except Animal.DoesNotExist:
            return JsonResponse({'error': 'Animal not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)





@csrf_exempt
def animal_delete(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            animal_id = data.get('animal_id')
            if animal_id is None:
                return JsonResponse({'success': False, 'error': 'Animal ID not provided in the request body.'}, status=400)
            animal = Animal.objects.get(id=animal_id)
            animal.delete()
            return JsonResponse({'success': True, 'message': 'Animal deleted successfully.'}, status=204)
        except Animal.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Animal not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
