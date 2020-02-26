import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage

from apis.api_view.utility import *
from apis.models import Expenses, Users, Companies
from django.db.models import Q, Sum

from django.utils import translation

@api_view(['GET'])
def expenseMonthList(request):
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
        userId = request.query_params.get('user_id')
        userId = None if userId is None else int(userId)
        assignerId = request.query_params.get('assigner_id')
        assignerId = None if assignerId is None else int(assignerId)
        strCycleType = request.query_params.get('cycle_type')
        if strCycleType is None or strCycleType == '':
            cycleType = 0
        else:
            cycleType = int(strCycleType)
        str_wants_currency = request.query_params.get('wants_currency')
        if str_wants_currency is None or str_wants_currency == '':
            wants_currency = 3
        else:
            wants_currency = int(str_wants_currency)

        currentYear = datetime.datetime.now().year
        month_info = []

        for i in range(12):
            month = i + 1
            if cycleType == 1:
                startDate = first_day_in_month(currentYear, month, 1)
                endDate = last_day_in_month(currentYear, month, 1)
                expensesByMonth = getMonthInfoForExpenses(startDate, endDate, userId, assignerId)
                expenseCount = getMonthInfoCountForExpenses(startDate, endDate, userId, assignerId)
                if expenseCount != 0:
                    total = getMonthTotalPrice(expensesByMonth, wants_currency)
                    monthHistory = {"month": month, "half": 1, "total_amount": total}
                    month_info.append(monthHistory)

                startDate = first_day_in_month(currentYear, month, 2)
                endDate = last_day_in_month(currentYear, month, 2)
                expensesByMonth = getMonthInfoForExpenses(startDate, endDate, userId, assignerId)
                expenseCount = getMonthInfoCountForExpenses(startDate, endDate, userId, assignerId)
                if expenseCount != 0:
                    total = getMonthTotalPrice(expensesByMonth, wants_currency)
                    monthHistory = {"month": month, "half": 2, "total_amount": total}
                    month_info.append(monthHistory)

            else:
                startDate = first_day_in_month(currentYear, month, 0)
                endDate = last_day_in_month(currentYear, month, 0)
                expensesByMonth = getMonthInfoForExpenses(startDate, endDate, userId, assignerId)
                expenseCount = getMonthInfoCountForExpenses(startDate, endDate, userId, assignerId)
                if expenseCount == 0:
                    continue

                total = getMonthTotalPrice(expensesByMonth, wants_currency)
                monthHistory = {"month": month, "total_amount": total}
                month_info.append(monthHistory)

    return Response(data={'success': True, 'data': month_info}, status=status.HTTP_200_OK)


@api_view(['GET'])
def expenseMonthListByStatus(request):
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
        userId = request.query_params.get('user_id')
        userId = None if userId is None else int(userId)
        assignerId = request.query_params.get('assigner_id')
        assignerId = None if assignerId is None else int(assignerId)
        strCycleType = request.query_params.get('cycle_type')
        if strCycleType is None or strCycleType == '':
            cycleType = 0
        else:
            cycleType = int(strCycleType)

        str_wants_currency = request.query_params.get('wants_currency')
        if str_wants_currency is None or str_wants_currency == '':
            wants_currency = 3
        else:
            wants_currency = int(str_wants_currency)

        str_exp_status = request.query_params.get('status')  #exp_status - status of expense (1: Submitted, 2: Processing, 3: Approved, 4: Reimbursed, 5: Closed)
        if str_exp_status is None or str_exp_status == '':
            exp_status = 1
        else:
            exp_status = int(str_exp_status)

        currentYear = datetime.datetime.now().year
        month_info = []

        for i in range(12):
            month = i + 1
            if cycleType == 1:
                startDate = first_day_in_month(currentYear, month, 1)
                endDate = last_day_in_month(currentYear, month, 1)
                expensesByMonth = getMonthInfoForExpensesByStatus(startDate, endDate, userId, assignerId, exp_status)
                expenseCount = getMonthInfoCountForExpensesByStatus(startDate, endDate, userId, assignerId, exp_status)
                if expenseCount != 0:
                    total = getMonthTotalPrice(expensesByMonth, wants_currency)
                    monthHistory = {"month": month, "half": 1, "total_amount": total}
                    month_info.append(monthHistory)

                startDate = first_day_in_month(currentYear, month, 2)
                endDate = last_day_in_month(currentYear, month, 2)
                expensesByMonth = getMonthInfoForExpensesByStatus(startDate, endDate, userId, assignerId, exp_status)
                expenseCount = getMonthInfoCountForExpensesByStatus(startDate, endDate, userId, assignerId, exp_status)
                if expenseCount != 0:
                    total = getMonthTotalPrice(expensesByMonth, wants_currency)
                    monthHistory = {"month": month, "half": 2, "total_amount": total}
                    month_info.append(monthHistory)

            else:
                startDate = first_day_in_month(currentYear, month, 0)
                endDate = last_day_in_month(currentYear, month, 0)
                expensesByMonth = getMonthInfoForExpensesByStatus(startDate, endDate, userId, assignerId, exp_status)
                expenseCount = getMonthInfoCountForExpensesByStatus(startDate, endDate, userId, assignerId, exp_status)
                if expenseCount == 0:
                    continue

                total = getMonthTotalPrice(expensesByMonth, wants_currency)
                monthHistory = {"month": month, "total_amount": total}
                month_info.append(monthHistory)

    return Response(data={'success': True, 'data': month_info}, status=status.HTTP_200_OK)


@api_view(['GET'])
def expenseByMonth(request, month):
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

    if month is None or month == '':
        month = 1

    if request.method == 'GET':
        userId = request.query_params.get('user_id')
        userId = None if userId is None else int(userId)
        assignerId = request.query_params.get('assigner_id')
        assignerId = None if assignerId is None else int(assignerId)
        strCycleType = request.query_params.get('cycle_type')
        if strCycleType is None or strCycleType == '':
            cycleType = 0
        else:
            cycleType = int(strCycleType)

        str_wants_currency = request.query_params.get('wants_currency')
        if str_wants_currency is None or str_wants_currency == '':
            wants_currency = 3
        else:
            wants_currency = int(str_wants_currency)

        currentYear = datetime.datetime.now().year
        month_info = []

        if cycleType == 1:
            startDate = first_day_in_month(currentYear, month, 1)
            endDate = last_day_in_month(currentYear, month, 1)
            expenses_data1 = getExpenseByMonth(startDate, endDate, userId, assignerId)
            dataExpense_1 = getExpenseData(expenses_data1, 1, wants_currency)

            startDate = first_day_in_month(currentYear, month, 2)
            endDate = last_day_in_month(currentYear, month, 2)
            expenses_data2 = getExpenseByMonth(startDate, endDate, userId, assignerId)
            dataExpense_2 = getExpenseData(expenses_data2, 2, wants_currency)

            month_info = dataExpense_1 + dataExpense_2
        else:
            startDate = first_day_in_month(currentYear, month, 0)
            endDate = last_day_in_month(currentYear, month, 0)
            expenses_data0 = getExpenseByMonth(startDate, endDate, userId, assignerId)
            dataExpense_0 = getExpenseData(expenses_data0, 0, wants_currency)

            month_info = dataExpense_0

    return Response(data={'success': True, 'data': month_info}, status=status.HTTP_200_OK)


@api_view(['GET'])
def expenseByMonthStatus(request, month):
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

    if month is None or month == '':
        month = 1

    if request.method == 'GET':
        userId = request.query_params.get('user_id')
        userId = None if userId is None else int(userId)
        assignerId = request.query_params.get('assigner_id')
        assignerId = None if assignerId is None else int(assignerId)
        strCycleType = request.query_params.get('cycle_type')
        if strCycleType is None or strCycleType == '':
            cycleType = 0
        else:
            cycleType = int(strCycleType)

        str_wants_currency = request.query_params.get('wants_currency')
        if str_wants_currency is None or str_wants_currency == '':
            wants_currency = 3 #default
        else:
            wants_currency = int(str_wants_currency)

        str_order_by = request.query_params.get(
            'order_by')  # order by - newest to oldest:0, oldest to newest:1, by merchant name:2
        if str_order_by is None or str_order_by == '':
            order_by = 0 # default
        else:
            order_by = int(str_order_by)

        str_exp_status = request.query_params.get(
            'status')  # exp_status - status of expense (1: Submitted, 2: Processing, 3: Approved, 4: Reimbursed, 5: Closed)
        if str_exp_status is None or str_exp_status == '':
            exp_status = 1 # default
        else:
            exp_status = int(str_exp_status)

        currentYear = datetime.datetime.now().year
        month_info = []

        if cycleType == 1:
            startDate = first_day_in_month(currentYear, month, 1)
            endDate = last_day_in_month(currentYear, month, 1)
            expenses_data1 = getExpenseByMonthStatus(startDate, endDate, userId, assignerId, exp_status, order_by)
            dataExpense_1 = getExpenseData(expenses_data1, 1, wants_currency)

            startDate = first_day_in_month(currentYear, month, 2)
            endDate = last_day_in_month(currentYear, month, 2)
            expenses_data2 = getExpenseByMonthStatus(startDate, endDate, userId, assignerId, exp_status, order_by)
            dataExpense_2 = getExpenseData(expenses_data2, 2, wants_currency)

            month_info = dataExpense_1 + dataExpense_2
        else:
            startDate = first_day_in_month(currentYear, month, 0)
            endDate = last_day_in_month(currentYear, month, 0)
            expenses_data0 = getExpenseByMonthStatus(startDate, endDate, userId, assignerId, exp_status, order_by)
            dataExpense_0 = getExpenseData(expenses_data0, 0, wants_currency)

            month_info = dataExpense_0

    return Response(data={'success': True, 'data': month_info}, status=status.HTTP_200_OK)


@api_view(['POST'])
def expenseSave(request):
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
        merchant_name = request.data.get('merchant_name')
        receipt_date = request.data.get('receipt_date')
        description = request.data.get('description')
        total_amount = request.data.get('total_amount')
        currency_type = request.data.get('currency_type')
        category = request.data.get('category')
        assignees = request.data.get('assignees')
        file_urls = request.data.get('file_urls')
        file_names = request.data.get('file_names')
        user_id = request.data.get('user_id')
        report_id = request.data.get('report_id')
        company_id = request.data.get('company_id')
        statusNum = request.data.get('status')

        user = Users.objects.get(pk=user_id)
        company = Companies.objects.get(pk=company_id)

        expense = None
        if statusNum == 0:
            expense = Expenses(
                merchant_name=merchant_name,
                receipt_date=receipt_date,
                description=description,
                total_amount=total_amount,
                currency_type=currency_type,
                category=category,
                assignees=assignees,
                file_urls=file_urls,
                file_names=file_names,
                user_id=user_id,
                report_id=report_id,
                company_id=company_id,
                status=statusNum,
                payments_currency=user.payments_currency
            )
        elif statusNum == 1:
            expense = Expenses(
                merchant_name=merchant_name,
                receipt_date=receipt_date,
                description=description,
                total_amount=total_amount,
                currency_type=currency_type,
                category=category,
                assignees=assignees,
                file_urls=file_urls,
                file_names=file_names,
                user_id=user_id,
                open_user_id = company.open_user_id,
                processing_user_id = company.processing_user_id,
                approve_user_id = company.approve_user_id,
                reimburse_user_id = company.reimburse_user_id,
                report_id=report_id,
                company_id=company_id,
                status=statusNum,
                payments_currency=user.payments_currency
            )
        else:
            return Response(data={'success': False, 'error': [translation.gettext('Error in creating Expense.')]}, status=status.HTTP_200_OK)

        try:
            expense.save()
        except Expenses.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in creating Expense.')]}, status=status.HTTP_200_OK)

        expenseData = getExpenseDetail([expense, ])

    return Response(data={'success': True, 'data': expenseData}, status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
def expenseUpdate(request, pk):
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

    expense = None
    try:
        expense = Expenses.objects.get(pk=pk)
    except Expenses.DoesNotExist:
        return Response(data={'success': False, 'error': [translation.gettext('Expense do not exist.')]},
                        status=status.HTTP_200_OK)

    if request.method == 'PUT':
        if int(expense.status) > 0:
            return Response(data={'success': False, 'error': [translation.gettext('Expense do not exist.')]},
                        status=status.HTTP_200_OK)
        
        merchant_name = request.data.get('merchant_name')
        receipt_date = request.data.get('receipt_date')
        description = request.data.get('description')
        total_amount = request.data.get('total_amount')
        currency_type = request.data.get('currency_type')
        category = request.data.get('category')
        assignees = request.data.get('assignees')
        file_urls = request.data.get('file_urls')
        file_names = request.data.get('file_names')
        user_id = request.data.get('user_id')
        report_id = request.data.get('report_id')
        company_id = request.data.get('company_id')
        statusNum = request.data.get('status')

        user = Users.objects.get(pk=user_id)
        company = Companies.objects.get(pk=company_id)

        if statusNum == 0:
            expense.merchant_name = merchant_name
            expense.receipt_date = receipt_date
            expense.description = description
            expense.total_amount = total_amount
            expense.currency_type = currency_type
            expense.category = category
            expense.assignees = assignees
            expense.file_urls = file_urls
            expense.file_names = file_names
            expense.user_id = user_id
            expense.report_id = report_id
            expense.company_id = company_id
            expense.status = statusNum
            expense.payments_currency = user.payments_currency
        elif statusNum == 1:
            expense.merchant_name = merchant_name
            expense.receipt_date = receipt_date
            expense.description = description
            expense.total_amount = total_amount
            expense.currency_type = currency_type
            expense.category = category
            expense.assignees = assignees
            expense.file_urls = file_urls
            expense.file_names = file_names
            expense.user_id = user_id
            expense.open_user_id = company.open_user_id,
            expense.processing_user_id = company.processing_user_id,
            expense.approve_user_id = company.approve_user_id,
            expense.reimburse_user_id = company.reimburse_user_id,
            expense.report_id = report_id
            expense.company_id = company_id
            expense.status = statusNum
            expense.payments_currency = user.payments_currency
        else
            return Response(data={'success': False, 'error': [translation.gettext('Error in creating Expense.')]}, status=status.HTTP_200_OK)

        defaultAssignees = []
        if company.open_user_id != None:
            defaultAssignees.append(company.open_user_id)
        if company.processing_user_id != None:
            defaultAssignees.append(company.processing_user_id)
        if company.approve_user_id != None:
            defaultAssignees.append(company.approve_user_id)
        if company.reimburse_user_id != None:
            defaultAssignees.append(company.reimburse_user_id)        

        try:
            expense.save()
        except Expenses.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in updating Expense.')]}, status=status.HTTP_200_OK)

        expenseData = getExpenseDetail([expense, ])

        return Response(data={'success': True, 'data': expenseData}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if int(expense.status) > 1:
            return Response(data={'success': False, 'error': [translation.gettext('Expense do not exist.')]},
                        status=status.HTTP_200_OK)
        
        if expense.file_urls != None:
            filePath = str(expense.file_urls)
            filePath = filePath.replace("/media/", "")

            if len(filePath) > 0:
                fs = FileSystemStorage()
                fs.delete(filePath)

        try:
            expense.delete()
        except Expenses.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in deleting Expense.')]}, status=status.HTTP_200_OK)

        return Response(data={'success': True}, status=status.HTTP_200_OK)


@api_view(['POST'])
def expenseChangeStatus(request):
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
        id = request.data.get('id')
        statusNum = request.data.get('status')

        try:
            expense = Expenses.objects.get(id=id)
        except Expenses.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Expense do not exist.')]},
                            status=status.HTTP_200_OK)

        expense.status = statusNum

        try:
            expense.save()
        except Expenses.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in updating Expense Status.')]}, status=status.HTTP_200_OK)

    return Response(data={'success': True}, status=status.HTTP_200_OK)

@api_view(['GET'])
def expenseCount(request):
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

    assigneeId = request.query_params.get('assignee_id')
    user_id = request.data.get('user_id')
    expense_status = request.query_params.get('status')
    
    countData = getCountForStatus(assigneeId, expense_status)
    return Response(data={'success': True, 'data': {'count': countData}}, status=status.HTTP_200_OK)

@api_view(['GET'])
def expensesInReport(request, report):
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

    assigneeId = request.query_params.get('assignee_id')
    wants_currency = request.query_params.get('wants_currency')
    expense_status = request.query_params.get('status')
    order_by = request.query_params.get('order_by')
    page = request.query_params.get('page')
    per_page = request.query_params.get('per_page')

    if wants_currency == None:
        wants_currency = 3

    expenseData = []
    oExpense = Expenses.objects.filter(Q(report_id=report))
    if expense_status != None:
        oExpense = oExpense.filter(Q(status=expense_status))

    if assigneeId != None:
        assignee = assigneeId
        oExpense = oExpense.filter(Q(assignees=assignee) | Q(assignees__startswith=assignee + ",") | Q(assignees__endswith="," + assignee) | Q(assignees__contains="," + assignee + ","))

    if order_by != None:
        oExpense = oExpense.order_by(order_by)

    expenses = oExpense.all()
    expenseData = getExpenseData(expenses, wants_currency)
    return Response(data={'success': True, 'data': expenseData}, status=status.HTTP_200_OK)
