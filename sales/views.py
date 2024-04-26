from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Sale
import json

@csrf_exempt
def sell_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity_sold = data.get('quantity_sold')
            
            if product_id is None or quantity_sold is None:
                return JsonResponse({'error': 'Product ID and quantity sold are required'}, status=400)
            
            product = Product.objects.get(id=product_id)
            sale = product.sell(quantity_sold)
            
            return JsonResponse({'message': 'Sale registered successfully', 'sale_id': sale.id}, status=201)
        
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
