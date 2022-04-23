from django.urls import path

from .views import logout_user

app_name = 'account'

urlpatterns = [
    path('logout/', logout_user, name='logout'),
]
