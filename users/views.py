from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from users.providers import create_user_by_credentials, get_or_create_token_by_user

@method_decorator(csrf_exempt, name='dispatch')
class RegisterAndGetTokenAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        user = create_user_by_credentials(username=username, password=password, email=email)
        token = get_or_create_token_by_user(user=user)

        return Response({'token': token.key})