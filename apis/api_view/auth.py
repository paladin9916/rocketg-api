import binascii
import os

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from RocketG_api import settings
from apis.api_view.utility import getUserData
from apis.models import Users

from django.utils import translation


@api_view(['POST'])
def signIn(request):
    if request.method == 'POST':
        token = request.headers.get('access-token')
        client = request.headers.get('client')
        uid = request.headers.get('uid')
        lang = request.headers.get('lang')
        if lang is not None:
            if lang == 'zh':
                translation.activate('ch')
            else:
                translation.activate(lang)
        elif lang is None or lang == '':
            lang = 'en'

        email = request.POST.get('email')
        password = request.POST.get('password')
        salt = settings.SECRET_KEY
        encrypted_pw = make_password(password, salt=salt)
        try:
            login_user = Users.objects.get(email=email, encrypted_password=encrypted_pw)
        except Users.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Invalid login credentials. Please try again.')]},
                            status=status.HTTP_200_OK)

        # Auth Token
        client = binascii.hexlify(os.urandom(20)).decode()
        # Session
        request.session['client'] = client
        request.session['uid'] = login_user.uid
        resultUserData = getUserData([login_user, ])[0]
        return Response(data={'success': True, 'data': resultUserData}, status=status.HTTP_200_OK, headers={'client': client, 'uid': login_user.uid})


@api_view(['DELETE'])
def signOut(request):
    if request.method == 'DELETE':
        client = request.headers.get('client')
        uid = request.headers.get('uid')
        lang = request.headers.get('lang')
        if lang is not None:
            if lang == 'zh':
                translation.activate('ch')
            else:
                translation.activate(lang)
        elif lang is None or lang == '':
            lang = 'en'
 
        try:
            if uid == request.session['uid'] and client == request.session['client']:
                del request.session['uid']
                del request.session['client']
        except KeyError:
            return Response(data={'success': True}, status=status.HTTP_200_OK)
            # return Response(data={'success': False, 'error': [translation.gettext('Error in signing out')]},
            #                 status=status.HTTP_200_OK)

        return Response(data={'success': True}, status=status.HTTP_200_OK)


@api_view(['POST'])
def checkEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        lang = request.headers.get('lang')
        if lang is not None:
            if lang == 'zh':
                translation.activate('ch')
            else:
                translation.activate(lang)
        elif lang is None or lang == '':
            lang = 'en'

        try:
            Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({'success': False, 'error': [translation.gettext('This email do not exist.')]},
                                status=status.HTTP_200_OK)

        return Response({'success': True}, status=status.HTTP_200_OK)
