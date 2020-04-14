from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.api_view.utility import getPaylipData
from apis.models import Users, Paylips

from django.utils import translation

@api_view(['POST', 'GET'])
def paylips(request, user):
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

    if request.method == 'GET':
        pays = Paylips.objects.filter(Q(user_id=user)).order_by('name')
        data = getPaylipData(pays)

        return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.POST.get('name')
        file_url = request.POST.get('file_urls')

        paylip = Paylips(
            name=name,
            user_id=user,
            file_urls=file_url
        )

        try:
            paylip.save()
            u = Users.objects.get(id=user)
            u.paylips_count += 1
            u.save()
        except Users.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in creating company.')]}, status=status.HTTP_200_OK)

        return Response(data={'success': True, 'data': 'success'}, status=status.HTTP_200_OK)
