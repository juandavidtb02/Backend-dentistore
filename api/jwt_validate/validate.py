from rest_framework.exceptions import AuthenticationFailed

import jwt,datetime,re

def validar(token,request):
    g = re.match("^Bearer\s+(.*)", token)
    if not g:
        raise AuthenticationFailed('Error de autenticación! 01')

    try:
        token = g.group(1)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Error de autenticación! 02')

    id = payload['id']

    if f'{id}' not in  request.session:
        raise AuthenticationFailed('Error de autenticación! 03')
    
    #Se ha validado que el token existe y esta activo, por lo que se refresca para que el usuario pueda
    #realizar peticiones durante otros 30 minutos
    
    return payload

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
    request.session[f'{id}'] = new_token
    return new_token