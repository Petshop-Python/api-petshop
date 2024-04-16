from django.shortcuts import render
from product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Product
from django.http import JsonResponse
import json


@csrf_exempt
def list_products(request):
    products = Product.objects.all()
    data = [{'id':product.id,
             'product_code': product.product_code,
             'product_name': product.product_name,
             'quantity': product.quantity,
             'price': product.price} for product in products]
    return JsonResponse(data, safe=False)




@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product = Product.objects.create(
            product_code=data['product_code'],
            product_name=data['product_name'],
            quantity=data['quantity'],
            price=data['price']
        )
        return JsonResponse({'status': 'success', 'product_id': product.id})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)



@csrf_exempt
def update_product(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            product_id = data.get('id')
            if product_id is None:
                return JsonResponse({'error': 'Product ID not provided in the request body'}, status=400)
            
            product = Product.objects.get(id=product_id)
            product.product_code = data.get('product_code', product.product_code)
            product.product_name = data.get('product_name', product.product_name)
            product.quantity = data.get('quantity', product.quantity)
            product.price = data.get('price', product.price)
            product.save()

            serialized_product = {
                'id': product.id,
                'product_code': product.product_code,
                'product_name': product.product_name,
                'quantity': product.quantity,
                'price': product.price
            }
            return JsonResponse({'success': True, 'product': serialized_product})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)        



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