from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def order(request):
    token = request.headers.get('Authorization').split(' ')[1]
    if not Token.objects.filter(key=token).exists():
        return Response({'error': 'Unauthorized'}, status=401)
    data = request.data
    print(f"Received order: {data}")
    return Response({'status': 'success'})
