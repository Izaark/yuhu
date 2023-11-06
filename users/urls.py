from django.urls import path
from users.views import RegisterAndGetTokenAPIView

urlpatterns = [
    path('users', RegisterAndGetTokenAPIView.as_view(), name='user-auth'),
]
