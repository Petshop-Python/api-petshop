# views.py

from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User  
from .forms import CustomUserCreationForm
import json

@csrf_exempt
def registro_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = CustomUserCreationForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'success', 'user_id': user.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        # Tente autenticar com o nome de usuário
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            # Se a autenticação falhar com o nome de usuário, tente com o e-mail
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            login(request, user)

            return JsonResponse({'status': 'success', 'user_id': user.id, 'user_name': user.username})


        else:
            return JsonResponse({'status': 'error', 'message': 'Nome de usuário, e-mail ou senha inválidos.'}, status=400)
