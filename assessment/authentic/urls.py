from django.urls import path

from .views import *

urlpatterns = [
    
    
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('register/', Register.as_view()),
    path('checkauth/', AuthenticatedView.as_view())

    
]