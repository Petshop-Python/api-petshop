from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from django.utils import timezone
from .models import Sale
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
            unit_price = product.price  # Obtém o preço unitário do produto

            if quantity_sold <= 0:
                return JsonResponse({'error': 'Quantity sold must be a positive integer'}, status=400)

            if quantity_sold > product.quantity:
                return JsonResponse({'error': 'Not enough quantity available for sale'}, status=400)

            # Atualiza a quantidade disponível do produto
            product.quantity -= quantity_sold
            product.save()

            # Verifica se já existe uma venda para este produto
            sale = Sale.objects.filter(product=product).first()

            if sale:
                # Se existir, atualiza a venda existente
                sale.quantity_sold += quantity_sold
                sale.total_price += quantity_sold * unit_price
                sale.update_date = timezone.now()  # Atualiza a data de atualização
                sale.save()
            else:
                # Se não existir, cria uma nova instância de Sale
                sale = Sale.objects.create(
                    product=product,
                    unit_price=unit_price,
                    quantity_sold=quantity_sold,
                    total_price=quantity_sold * unit_price
                )

            return JsonResponse({'message': 'Sale registered successfully', 'sale_id': sale.id}, status=201)

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def list_sales(request):
    if request.method == 'GET':
        # Obtém os parâmetros de consulta para o mês e ano, se fornecidos
        month = request.GET.get('month')
        year = request.GET.get('year')

        # Consulta todas as vendas no banco de dados
        sales = Sale.objects.all()

        # Filtra as vendas se o mês e o ano forem fornecidos
        if month and year:
            try:
                month = int(month)
                year = int(year)
                sales = sales.filter(sale_date__year=year, sale_date__month=month)
            except ValueError:
                return JsonResponse({'error': 'Invalid month or year format'}, status=400)

        # Lista para armazenar os dados serializados de cada venda
        serialized_sales = []

        # Itera sobre cada venda e serializa todos os campos
        for sale in sales:
            serialized_sale = {
                'id': sale.id,
                'product_id': sale.product.id,
                'product_name': sale.product.product_name,
                'quantity_sold': sale.quantity_sold,
                'total_price': str(sale.total_price),
                'unit_price': str(sale.unit_price),
                'sale_date': sale.sale_date.strftime('%Y-%m-%d'),
                'create_date': sale.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                'update_date': sale.update_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            serialized_sales.append(serialized_sale)

        # Retorna os dados serializados como uma resposta JSON
        return JsonResponse(serialized_sales, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


@csrf_exempt
def delete_all_sales(request):
    if request.method == 'DELETE':
        try:
            # Exclui todos os registros da tabela Sale
            Sale.objects.all().delete()
            return JsonResponse({'message': 'All sales deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)