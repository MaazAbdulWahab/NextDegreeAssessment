from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions  import IsAuthenticated
from core.utils import CustomTokenAuth



# Create your views here.


class Register(APIView):

    authentication_classes=[]
    
    permission_classes=[]

    def post(self, request, *args, **kwargs):
        
        username= request.data.get('username')
        email= request.data.get('email')
        password= request.data.get('password')

        if User.objects.filter(username=username, email=email).exists():
           return Response({'success': False, 'message': 'Already Exists'},
                    status=400) 

        user= User.objects.create(username=username, email=email)

        user.set_password(password)
        user.save()

        token, created=Token.objects.get_or_create(user=user)
        

        return Response({'success': True, 'token':token.key}, status=201)

    


class Login(APIView):
    authentication_classes=[]
    
    permission_classes=[]
    
    def post(self, request, *args, **kwargs):
        
        email= request.data.get('email')
        password= request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'No Matching User Found'},
                    status=404)

        valid = user.check_password(password)

        if valid:
            token, created=Token.objects.get_or_create(user=user)
            return Response({'success': True, 'message': 'Successfully Logged In',
            'token':token.key},
                    status=200)

        else:
            return Response({'success': False, 'message': 'Wrong Password'},
                    status=400)



class Logout(APIView):
    authentication_classes=[TokenAuthentication]
    
    permission_classes=[IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        

        token =Token.objects.get(user=request.user)

        token.delete()

        return Response({'success': True, 'message': 'Logged Out'},
                    status=200)


class AuthenticatedView(APIView):
    authentication_classes=[CustomTokenAuth]
    
    permission_classes=[IsAuthenticated]


    def get(self,request, *args, **kwargs):

        return Response({'success': True,'message':'Auth Success'}, status=200)





