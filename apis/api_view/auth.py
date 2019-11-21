import binascii
import os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.api_view.data_manage import getUserData
from apis.models import Users


@api_view(['POST'])
def signIn(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            login_user = Users.objects.get(email=email, encrypted_password=password)
        except Users.DoesNotExist:
            login_user = None

        if login_user == None:
            return Response(data={'success': False, 'error': ['Invalid login credentials. Please try again.']},
                                status=status.HTTP_200_OK)

        # Auth Token
        token_key = binascii.hexlify(os.urandom(20)).decode()
        login_user.tokens = token_key
        login_user.save()

        resultUserData = getUserData([login_user, ])[0]
        return Response(data={'data': resultUserData}, status=status.HTTP_200_OK, headers={'access-token': token_key, 'client': login_user.provider, 'uid': login_user.uid})


@api_view(['DELETE'])
def signOut(request):
    if  request.method == 'DELETE':
        token = request.headers.get('access-token')
        client = request.headers.get('client')
        uid = request.headers.get('uid')

        try:
            auth_user = Users.objects.get(tokens=token)
            auth_user.tokens = ''
            auth_user.provider = ''
            auth_user.uid = ''
            auth_user.save()
        except Users.DoesNotExist:
            return Response(data={'success': False, 'error': ['Error in signing out']},
                            status=status.HTTP_200_OK)

        return Response(data={'success': True}, status=status.HTTP_200_OK)


@api_view(['POST'])
def checkEmail(request):
    if request.method == 'POST':
        email = request.data.get('email')

        try:
            login_user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            login_user = None

        if login_user == None:
            return Response({'status': 'error', 'error_code': 10002},
                                status=status.HTTP_200_OK)
        else:
            return Response({'state': 'success', 'error_code': 0}, status=status.HTTP_200_OK)