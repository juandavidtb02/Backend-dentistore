from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializer import UserSerializer,CategoriesSerializer
from .models import Users,Categories
from .jwt_validate.validate import validar,refresh_token

import jwt,datetime,re


class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = Users.objects.filter(usermail=email).first()

        if user is None:
            raise AuthenticationFailed('Datos de usuario incorrectos!')
            
        if not user.check_password(password):
            raise AuthenticationFailed('Datos de usuario incorrectos!')

        
        payload = {
            'id':user.userid,
            'usermail':user.usermail,
            'role':user.userrole,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret', algorithm='HS256')

        response = Response()
        id = user.userid
        request.session[f'{id}'] = token
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):
    def get(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')

        payload = validar(token,request)
        new_token = refresh_token(payload,request)
        user = Users.objects.filter(userid=payload['id']).first()
        serializer = UserSerializer(user)
        response = Response()
        response.data = {
            'data': serializer.data,
            'token':new_token
        }
        return response

class LogoutView(APIView):
    def post(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        g = re.match("^Bearer\s+(.*)", token)

        if not g:
            raise AuthenticationFailed('La sesión no existe! Error 01')

        try:
            token = g.group(1)
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('La sesión no existe! Error 02')

        id = payload['id']
        if f'{id}' in request.session:
            del request.session[f'{id}']
        else: 
            raise AuthenticationFailed('La sesión no existe! Error 03')
        
        response = Response()
        
        response.data = {
            'message':'Sesion cerrada'
        }
        return response

class CategoriesView(APIView):
    def get(self,request):
        datos = Categories.objects.values()
        serializer = CategoriesSerializer(datos,many=True)
        return Response(serializer.data)

# Create your views here.
