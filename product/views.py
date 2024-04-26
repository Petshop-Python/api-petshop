from django.shortcuts import render
from product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Product
from django.http import JsonResponse
from django.utils import timezone
import json


@csrf_exempt
def list_products(request):
    products = Product.objects.all()
    data = [{'id': product.id,
             'product_code': product.product_code,
             'product_name': product.product_name,
             'quantity': product.quantity,
             'price': product.price,
             'entry_date': product.create_date.strftime("%Y-%m-%d") if product.create_date else None,
             'update_date': product.update_date.strftime("%Y-%m-%d") if product.update_date else None} for product in products]  
    return JsonResponse(data, safe=False)




@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            # Convertendo os dados do corpo da solicitação para um dicionário Python
            data = json.loads(request.body)
            
            # Criando uma nova instância de Product com os dados fornecidos
            new_product = Product.objects.create(
                product_code=data['product_code'],
                product_name=data['product_name'],
                quantity=data['quantity'],
                price=data['price']
                # Se quiser definir create_date automaticamente, remova o campo daqui
            )
            
            # Retornando uma resposta de sucesso com os dados do novo produto criado
            return JsonResponse({'message': 'Product created successfully', 'product_id': new_product.id}, status=201)
        
        except KeyError:
            # Se algum dos campos obrigatórios estiver ausente nos dados da solicitação
            return JsonResponse({'error': 'One or more required fields are missing'}, status=400)
        
        except Exception as e:
            # Lidando com outros erros inesperados
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Retornando um erro se a solicitação não for POST
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



@csrf_exempt
def update_product(request):
    if request.method == 'PUT':
        try:
            # Convertendo os dados do corpo da solicitação para um dicionário Python
            data = json.loads(request.body)
            
            # Obtendo o product_id do corpo da solicitação
            product_id = data.get('id')
            
            # Verificando se o product_id foi fornecido
            if product_id is None:
                return JsonResponse({'error': 'Product ID is missing in the request body'}, status=400)
            
            # Recuperando o objeto Product existente pelo ID
            product = Product.objects.get(id=product_id)
            
            # Atualizando os campos do objeto Product com os novos dados fornecidos
            product.product_code = data.get('product_code', product.product_code)
            product.product_name = data.get('product_name', product.product_name)
            product.quantity = data.get('quantity', product.quantity)
            product.price = data.get('price', product.price)
            
            # Atualizando a data de atualização para o tempo atual
            product.update_date = timezone.now()
            
            # Salvando as alterações no banco de dados
            product.save()
            
            # Retornando uma resposta de sucesso com os dados atualizados do produto
            return JsonResponse({'message': 'Product updated successfully', 'product_id': product.id}, status=200)
        
        except Product.DoesNotExist:
            # Se o produto com o ID especificado não existir
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        except Exception as e:
            # Lidando com outros erros inesperados
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Retornando um erro se a solicitação não for PUT
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)



@csrf_exempt
def delete_product(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            if product_id is None:
                return JsonResponse({'success': False, 'error': 'Product ID not provided in the request body.'}, status=400)
            
            product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({'success': True, 'message': 'Product deleted successfully.'}, status=204)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)     