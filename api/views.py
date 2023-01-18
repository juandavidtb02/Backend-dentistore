from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializer import UserSerializer,CategoriesSerializer,ProductsSerializer
from .models import Users,Categories,UserLog,Products
from .jwt_validate.validate import validar,refresh_token,its_admin
from django.conf import settings

import jwt,datetime,re
import base64

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
        uid = user.userid
        try:
            log = UserLog.objects.create(id=uid,token=token)
        except:
            raise AuthenticationFailed('Usuario ya se encuentra logeado!')
            

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
            UserLog.objects.filter(token=token).delete()
            raise AuthenticationFailed('La sesión no existe! Error 02')
        id = payload['id']
        user = UserLog.objects.filter(id=id).first()

        try:
            UserLog.objects.filter(id=id).delete()
            if id == user.id:
                response = Response()
        
            response.data = {
                'message':'Sesion cerrada'
            }
        except:
            raise AuthenticationFailed('La sesión no existe! Error 03')
        return response

class CategoriesView(APIView):
    def get(self,request):
        datos = Categories.objects.values()
        serializer = CategoriesSerializer(datos,many=True)
        return Response(serializer.data)

    def post(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        category_name = request.data['category_name']
        category_image = request.data['image']
        if category_image != '':
            with category_image.open("rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
        

        response = Response()
        if(its_admin(new_token)):
            
            try:
                Categories.objects.create(category_name=category_name,image=encoded_string)
            except:
                response.data = {
                'message' : 'Error al registrar categoria',
                'token':new_token
                }
                response.status_code = 500
                return response

            response.data = {
                'message' : 'Categoria registrada exitosamente',
                'token':new_token
            }

        return response



class ProductsView(APIView):
    def get(self,request):
        datos = Products.objects.values()
        serializer = ProductsSerializer(datos,many=True)
        return Response(serializer.data)


# Create your views here.
