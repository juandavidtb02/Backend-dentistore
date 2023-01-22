from rest_framework.exceptions import AuthenticationFailed
from ..models import UserLog,Users
import jwt,datetime,re

def validar(tokenu,request):
    g = re.match("^Bearer\s+(.*)", tokenu)
    if not g:
        raise AuthenticationFailed('Error de autenticación! 01')

    try:
        tokenu = g.group(1)
        payload = jwt.decode(tokenu, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        UserLog.objects.filter(token=tokenu).delete()
        raise AuthenticationFailed('Error de autenticación! 02')


    user = list(UserLog.objects.filter(token=tokenu).values())
    if len(user) == 0:
        raise AuthenticationFailed('Error de autenticación! 03')
    
    
    return payload

    #Se ha validado que el token existe y esta activo, por lo que se refresca para que el usuario pueda
    #realizar peticiones durante otros 30 minutos
    
def refresh_token(payload,request):
    new_payload = {
        'id':payload['id'],
        'usermail':payload['usermail'],
        'role':payload['role'],
        'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'iat':datetime.datetime.utcnow()
    }
    new_token = jwt.encode(new_payload,'secret', algorithm='HS256')
    id = payload['id']
    user = UserLog.objects.filter(id=id).first()
    user.token = new_token
    user.save()
    return new_token

def its_admin(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Error de autenticación! 02')

    if (payload['role'] == 'admin'):    
        user = list(Users.objects.filter(usermail=payload['usermail'],userrole='admin').values())
        if len(user) == 0:
            raise AuthenticationFailed('Error de autenticacion! 03')
    else:
        raise AuthenticationFailed('Error de autencicacion! n_a')


    return True