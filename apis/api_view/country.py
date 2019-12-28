from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.api_view.utility import getCountryData
from apis.models import Country_locales

from django.utils import translation


@api_view(['GET'])
def countryGet(request):
    token = request.headers.get('access-token')
    client = request.headers.get('client')
    uid = request.headers.get('uid')
    lang = request.headers.get('lang')

    if lang is None or lang == '':
        lang = 'en'

    if request.method == 'GET':
        countryList = None
        try:
            countryList = Country_locales.objects.filter(Q(language=lang)).order_by('country_id')
        except Country_locales.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in getting country.')]}, status=status.HTTP_200_OK)

        countryData = getCountryData(countryList)
        return Response(data={'success': True, 'data': countryData}, status=status.HTTP_200_OK)