from django.utils import translation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from array import *

from apis.api_view.utility import getReportDetail, getReportData as utGetReportData, getUsersWithIds, getTotalForReports, exchangeMoney, getReportIdsForAssignee
from apis.models import Reports

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

    comment = request.data.get('comment')
    user_id = request.data.get('user_id')

    report = Reports(comment=comment, user_id=user_id)

    try:
        report.save()
    except Reports.DoesNotExist:
        return Response(data={'success': False, 'error': [translation.gettext('Error in creating report.')]}, status=status.HTTP_200_OK)
    reportData = getReportDetail([report, ])
    return Response(data={'success': True, 'data': reportData}, status=status.HTTP_200_OK)

def getReportData(reports, totals, wants_currency):
    reportData = []
    for report in reports:
        ntotal = 0
        nCount = 0
        for total in totals:
            if total["report_id"] == report["id"]:
                nCount += total["count"]
                ntotal += exchangeMoney(total["total_amount"], total["currency_type"], wants_currency)
        
        report["total_amount"] = ntotal
        report["count"] = nCount

    return reports

def reportList(request):
    reportData = []
    userId = request.query_params.get('user_id')
    assigneeId = request.query_params.get('assignee_id')
    wants_currency = request.query_params.get('wants_currency')
    expense_status = request.query_params.get('status')
    order_by = request.query_params.get('order_by')
    page = request.query_params.get('page')
    per_page = request.query_params.get('per_page')

    if wants_currency == None:
        wants_currency = 3

    if userId != None:
        oReports = Reports.objects.filter(user_id=userId)
        if order_by != None:
            oReports = oReports.order_by(order_by)
        
        reports = oReports.all()
        reportData = utGetReportData(reports)
        report_ids = []
        for report in reports:
            report_ids.append(report.id)
        
        totals = getTotalForReports(report_ids)
        
    elif assigneeId != None:
        report_ids = getReportIdsForAssignee(assigneeId, expense_status)
        oReports = Reports.objects.filter(id__in=report_ids)
        if order_by != None:
            oReports = oReports.order_by(order_by)

        reports = oReports.all()
        reportData = utGetReportData(reports)
        totals = getTotalForReports(report_ids, assigneeId, expense_status)

    reportData = getReportData(reportData, totals, wants_currency)
    return Response(data={'success': True, 'data': reportData}, status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
def reports(request):
    if request.method == 'POST':
        return reportSave(request)
    elif request.method == 'GET':
        return reportList(request)

@api_view(['DELETE'])
def deleteReport(request, pk):
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

    try:
        report = Reports.objects.get(pk=pk)
        report.delete()
    except Expenses.DoesNotExist:
        return Response(data={'success': False, 'error': [translation.gettext('Report do not exist.')]},
                        status=status.HTTP_200_OK)

    return Response(data={'success': True}, status=status.HTTP_200_OK)