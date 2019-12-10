import datetime
import calendar

from django.db.models import Q, Sum, Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.models import Expenses


@api_view(['GET'])
def expenseMonth(request):
    token = request.headers.get('access-token')
    client = request.headers.get('client')
    uid = request.headers.get('uid')
    lang = request.headers.get('lang')

    if lang is None or lang == '':
        lang = 'en'

    userId = int(request.query_params.get('user_id'))
    assignerId = int(request.query_params.get('assigner_id'))
    cycleType = int(request.query_params.get('cycle_type'))

    utc = 0.142013
    etc = 0.127317

    today = datetime.datetime.now()
    currentYear = today.year

    month_info = []

    for i in range(12):
        month = i + 1
        if cycleType == 1:
            startDate = first_day_in_month(currentYear, month, 1)
            endDate = last_day_in_month(currentYear, month, 1)
            expensesByMonth = getMonthInfoForExpenses(startDate, endDate, userId, assignerId)
            expenseCount = getMonthInfoCountForExpenses(startDate, endDate, userId, assignerId)
            if expenseCount != 0:
                total = getMonthTotalPrice(expensesByMonth, utc, etc)
                monthHistory = {"month": month, "half": 1, "total_amount": total}
                month_info.append(monthHistory)

            startDate = first_day_in_month(currentYear, month, 2)
            endDate = last_day_in_month(currentYear, month, 2)
            expensesByMonth = getMonthInfoForExpenses(startDate, endDate, userId, assignerId)
            expenseCount = getMonthInfoCountForExpenses(startDate, endDate, userId, assignerId)
            if expenseCount != 0:
                total = getMonthTotalPrice(expensesByMonth, utc, etc)
                monthHistory = {"month": month, "half": 2, "total_amount": total}
                month_info.append(monthHistory)

        else:
            startDate = first_day_in_month(currentYear, month, 0)
            endDate = last_day_in_month(currentYear, month, 0)
            expensesByMonth = getMonthInfoForExpenses(startDate, endDate, userId, assignerId)
            expenseCount = getMonthInfoCountForExpenses(startDate, endDate, userId, assignerId)
            if expenseCount == 0:
                continue

            total = getMonthTotalPrice(expensesByMonth, utc, etc)
            monthHistory = {"month": month, "total_amount": total}
            month_info.append(monthHistory)

    return Response(data={'success': True, 'data': month_info}, status=status.HTTP_200_OK)


def first_day_in_month(year, month, type):
    if type == 2:
        return datetime.datetime(year, month, 16)
    else:
        return datetime.datetime(year, month, 1)


def last_day_in_month(year, month, type):
    lastDay = calendar.monthrange(year, month)[1]  # last day of month
    if type == 1:
        return datetime.datetime(year, month, 15)
    else:
        return datetime.datetime(year, month, lastDay)


def getMonthInfoForExpenses(startDate, endDate, userId, assignerId):
    if userId:
        expensesByMonth = Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate),
                                                       Q(receipt_date__lte=endDate), Q(status__gt=0)).values(
            'currency_type').annotate(total_amount=Sum('total_amount'))
    elif assignerId:
        expensesByMonth = Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate),
                                                       Q(receipt_date__lte=endDate), Q(status__gt=0)).values(
            'currency_type').annotate(total_amount=Sum('total_amount'))

    return expensesByMonth


def getMonthInfoCountForExpenses(startDate, endDate, userId, assignerId):
    if userId:
        expensesCountByMonth = list(Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate), Q(receipt_date__lte=endDate)))
    elif assignerId:
        expensesCountByMonth = list(Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate), Q(receipt_date__lte=endDate)))
    count = len(expensesCountByMonth)
    return count


def getMonthTotalPrice(expensesByMonth, utc, etc):
    total = 0
    for expense in expensesByMonth:
        if expense['currency_type'] == 1:
            total += expense['total_amount'] / utc
        elif expense['currency_type'] == 2:
            total += expense['total_amount'] / etc
        elif expense['currency_type'] == 3:
            total += expense['total_amount']
    return total
