from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializer import UserSerializer,CategoriesSerializer,ProductsSerializer,ClientesSerializer
from .models import Users,Categories,UserLog,Products,Images_products
from .jwt_validate.validate import validar,refresh_token,its_admin
from django.conf import settings
from rest_framework.decorators import action

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
            'username':user.username,
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
            try:
                data_log = UserLog.objects.filter(id=uid).first()
                old_token = data_log.token
                payload = jwt.decode(old_token, 'secret', algorithms=['HS256'])
                raise AuthenticationFailed('Usuario ya se encuentra logeado!')
            except jwt.ExpiredSignatureError:
                UserLog.objects.filter(token=old_token).delete()
                log = UserLog.objects.create(id=uid,token=token)

        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):
    def post(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)
        user = Users.objects.filter(userid=payload['id']).first()
        UserSerializer(user)
        response = Response()
        response.data = {
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
    
class CategoriesNameView(APIView):
    def get(self,request):
        datos = Categories.objects.values('category_id','category_name')
        return Response(datos)

class CategoriesView(APIView):
    def get(self,request):
        datos = Categories.objects.values()
        serializer = CategoriesSerializer(datos,many=True)
        return Response(serializer.data)

    def post(self,request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        try:
            category_name = request.data['category_name']
            category_image = request.data['category_image']
            if category_image != '':
                with category_image.open("rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
        except Exception as e:
            response.data = {
                'message' : 'Error al registrar categoria',
                'token':new_token
                }
            response.status_code = 500
            
            
            return response



        
        if(its_admin(new_token)):
            
            try:
                Categories.objects.create(category_name=category_name,category_image=encoded_string.decode())
            except Exception as e:
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
        else:
            response.data = {
                'message' : 'El usuario no tiene los permisos necesarios',
                'token':new_token
            }
            response.status_code = 403
            

        return response
    def delete(self,request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        try:
            category_id = request.data['category_id']
        except Exception as e:
            response.data = {
                'message' : 'Error al borrar categoria',
                'token':new_token
                }
            response.status_code = 500
                
            
            return response

        if(its_admin(new_token) != True):
            response.data = {
            'message' : 'El usuario no tiene los permisos necesarios',
            'token':new_token
            }
            response.status_code = 403

            
            return response
    
        try:
            Categories.objects.filter(category_id=category_id).delete()
        except Exception as e:
            response.data = {
            'message' : 'Error al borrar categoria',
            'token':new_token
            }
            response.status_code = 500
            
            return response

        response.data = {
            'message' : 'Categoria eliminada correctamente',
            'token':new_token
        }


        return response

    def put(self,request):
        response = Response()

        

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        if(its_admin(new_token) != True):
            response.data = {
            'message' : 'El usuario no tiene los permisos necesarios',
            'token':new_token
            }
            response.status_code = 403
            
            return response

        try:
            category_id = request.data['category_id']
            category_name = request.data['category_name']
            newData = Categories.objects.filter(category_id=category_id).first()
            newData.category_name = category_name
            if(request.data['category_image'] != 'undefined'):
                category_image = request.data['category_image']
                with category_image.open("rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                newData.category_image = encoded_string.decode()
            newData.save()
        except Exception as e:
            print(e)
            response.data = {
                'message' : 'Error al borrar categoria',
                'token':new_token
                }
            response.status_code = 500
            return response
        
        response.data = {
            'message' : 'Categoria editada correctamente',
            'token':new_token
        }
        
        return response


class ClientsView(APIView):
    def get(self,request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        if(its_admin(new_token) != True):
            response.data = {
            'message' : 'El usuario no tiene los permisos necesarios',
            'token':new_token
            }
            response.status_code = 403
            
            return response
        
        objetos_filtrados = Users.objects.filter(userrole='usuario')
        serializado = ClientesSerializer(objetos_filtrados, many=True)
        response.data = {
            'data':serializado.data,
            'token':new_token
        }
        return response
    
    def delete(self,request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        try:
            userid = request.data['userid']
        except Exception as e:
            response.data = {
                'message' : 'Error al borrar usuario',
                'token':new_token
                }
            response.status_code = 500
                
            
            return response

        if(its_admin(new_token) != True):
            response.data = {
            'message' : 'El usuario no tiene los permisos necesarios',
            'token':new_token
            }
            response.status_code = 403

            
            return response
    
        try:
            Users.objects.filter(userid=userid).delete()
        except Exception as e:
            response.data = {
            'message' : 'Error al borrar usuario',
            'token':new_token
            }
            response.status_code = 500
            
            return response

        response.data = {
            'message' : 'Usuario eliminado correctamente',
            'token':new_token
        }


        return response


class ProductsView(APIView):
    def get(self, request):
        products = Products.objects.select_related('category').prefetch_related('images_products_set').all()
        data = []
        for product in products:
            images = []
            for image in product.images_products_set.all():
                images.append({
                    'image_id': image.image_id,
                    'image_name': image.image_name,
                    'image_text': image.image_text,
                })
            data.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_stock': product.product_stock,
                'product_image': product.product_image,
                'product_descrip': product.product_descrip,
                'product_details': product.product_details,
                'category': {
                    'category_id': product.category.category_id,
                    'category_name': product.category.category_name,
                    'category_image': product.category.category_image,
                },
                'images': images,
            })
        return Response(data)


    
    def post(self,request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        try:
            product_name = request.data['product_name']
            product_price = request.data['product_price']
            product_stock = request.data['product_stock']
            product_descrip = request.data['product_descrip']
            product_details = request.data['product_details']
            category_id = request.data['category_id']

        except Exception as e:
            print(e)
            response.data = {
                'message' : 'Error al registrar categoria',
                'token':new_token
                }
            response.status_code = 500
            
            return response
        
        if(its_admin(new_token) != True):
            response.data = {
            'message' : 'El usuario no tiene los permisos necesarios',
            'token':new_token
            }
            response.status_code = 403

            
            return response
        
        try:
            Products.objects.create(product_name=product_name,product_price=product_price,product_stock=product_stock,product_descrip=product_descrip,product_details=product_details,category_id=category_id)
        except Exception as e:
            response.data = {
            'message' : 'Error al crear categoria',
            'token':new_token
            }
            response.status_code = 500
            
            return response
        
        response.data = {
            'message' : 'Producto añadido correctamente',
            'token':new_token
        }


        return response
    
    def delete(self,request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        try:
            product_id = request.data['product_id']

        except Exception as e:
            print(e)
            response.data = {
                'message' : 'Error al eliminar producto',
                'token':new_token
                }
            response.status_code = 500
            
            return response
        
        if(its_admin(new_token) != True):
            response.data = {
            'message' : 'El usuario no tiene los permisos necesarios',
            'token':new_token
            }
            response.status_code = 403

            
            return response        

        try:
            Products.objects.filter(product_id=product_id).delete()
        except Exception as e:
            print(e)
            response.data = {
            'message' : 'Error al borrar producto o imagenes',
            'token':new_token
            }
            response.status_code = 500
            
            return response

        response.data = {
            'message' : 'Producto eliminado correctamente',
            'token':new_token
        }


        return response


class ImagesProductsView(APIView):
    def post(self,request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        try:
            image_name = request.data['image_name']
            image = request.data['image']
            product_id = request.data['product_id']
            with image.open("rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

        except Exception as e:
            print(e)
            response.data = {
                'message' : 'Error al registrar imagen',
                'token':new_token
                }
            response.status_code = 500
            
            return response
        
        if(its_admin(new_token) != True):
            response.data = {
            'message' : 'El usuario no tiene los permisos necesarios',
            'token':new_token
            }
            response.status_code = 403

            
            return response
        try:
            Images_products.objects.create(image_name=image_name,image_text=encoded_string.decode(),product_id=product_id)
        except Exception as e:
            response.data = {
            'message' : 'Error al crear imagen',
            'token':new_token
            }
            response.status_code = 500
            
            return response
        
        
        response.data = {
            'message' : 'Producto añadido correctamente',
            'token':new_token
        }

        return response

    def delete(self,request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        payload = validar(token,request)
        new_token = refresh_token(payload,request)

        try:
            image_id = request.data['image_id']

        except Exception as e:
            print(e)
            response.data = {
                'message' : 'Error al registrar categoria',
                'token':new_token
                }
            response.status_code = 500
            
            return response
        
        if(its_admin(new_token) != True):
            response.data = {
            'message' : 'El usuario no tiene los permisos necesarios',
            'token':new_token
            }
            response.status_code = 403

            
            return response        

        try:
            Images_products.objects.filter(image_id=image_id).delete()
        except Exception as e:
            response.data = {
            'message' : 'Error al borrar imagen',
            'token':new_token
            }
            response.status_code = 500
            
            return response

        response.data = {
            'message' : 'Imagen eliminada correctamente',
            'token':new_token
        }


        return response

        

        


# Create your views here.
