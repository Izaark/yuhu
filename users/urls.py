from django.urls import path
from users.views import RegisterAndGetTokenAPIView

urlpatterns = [
    path('user/', RegisterAndGetTokenAPIView.as_view(), name='user-auth'),
]
