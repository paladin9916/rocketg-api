from django.utils import translation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from apis.api_view.utility import getReportDetail
from apis.models import Reports


@api_view(['POST'])
def reportSave(request):
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

    if request.method == 'POST':
        comment = request.data.get('comment')
        user_id = request.data.get('user_id')

        report = Reports(comment=comment, user_id=user_id)

        try:
            report.save()
        except Reports.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in creating report.')]}, status=status.HTTP_200_OK)
        reportData = getReportDetail([report, ])
        return Response(data={'success': True, 'data': reportData}, status=status.HTTP_200_OK)