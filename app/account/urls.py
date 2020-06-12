from django.urls import path
from .views import CreateUserView, CreateTokenView
app_name = 'account'

urlpatterns = [
    path('register/', CreateUserView.as_view()),
    path('token/', CreateTokenView.as_view(), name='token'),

]