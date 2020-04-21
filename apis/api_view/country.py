from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.api_view.utility import getCountryData, isLoginUser
from apis.models import Country_locales

from django.utils import translation


@api_view(['GET'])
def countryGet(request):
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
    
    isLogin = isLoginUser(request)
    if isLogin == False:
        return Response(data={'code': 1, 'success': False, 'error': [translation.gettext('Your session expired, please log in.')]},
                        status=status.HTTP_200_OK)

    if request.method == 'GET':
        countryList = None
        try:
            countryList = Country_locales.objects.filter(Q(language=lang)).order_by('country_id')
        except Country_locales.DoesNotExist:
            return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Error in getting country.')]}, status=status.HTTP_200_OK)

        countryData = getCountryData(countryList)
        return Response(data={'code': 0, 'success': True, 'data': countryData}, status=status.HTTP_200_OK)