import calendar
import datetime
import requests

from django.db.models import Q, Sum, Count

from apis.api_view import constants
from apis.models import Industry_locales, Country_locales, Images, Countries, Expenses, Users
from apis.serializers import ImageSerializer

def getExpenseData(expenses, wants_currency):
    expensesList = []
    user_ids = []
    for expense in expenses:
        assignees = list(map(toInt, filter(toInt, str(expense.assignees).split(','))))
        expenseData = {
            "id": expense.id,
            "merchant_name": expense.merchant_name,
            "receipt_date": expense.receipt_date,
            "description": expense.description,
            "total_amount": expense.total_amount,
            "category": expense.category,
            "file_urls": expense.file_urls,
            "file_names": expense.file_names,
            "company_id": expense.company_id,
            "report_id": expense.report_id,
            "currency_type": expense.currency_type,
            "status": expense.status,
            "created_at": expense.created_at,
            "updated_at": expense.updated_at,            
            "converted_amount": exchangeMoney(expense.total_amount, expense.currency_type, wants_currency),
            "assignees_ids": assignees,
            "payments_currency": expense.payments_currency,
            "payments_amount": exchangeMoney(expense.total_amount, expense.currency_type, expense.payments_currency),
            "user_id": expense.user_id,
            "open_user_id": expense.open_user_id,
            "processing_user_id": expense.processing_user_id,
            "approve_user_id": expense.approve_user_id,
            "reimburse_user_id": expense.reimburse_user_id,
        }

        expensesList.append(expenseData)
        user_ids.append(int(expense.user_id))
        if expense.open_user_id != None:
            user_ids.append(int(expense.open_user_id))
        if expense.processing_user_id != None:
            user_ids.append(int(expense.processing_user_id))
        if expense.approve_user_id != None:
            user_ids.append(int(expense.approve_user_id))
        if expense.reimburse_user_id != None:
            user_ids.append(int(expense.reimburse_user_id))

        user_ids += assignees

    users = getUsersWithIds(user_ids)
    expensesData = []
    for expense in expensesList:
        user = [u for u in users if u.id == expense["user_id"]]
        user = getUserData(user)
        expense["user"] = user[0]
        expense["assignees"] = []
        for assignee_id in expense["assignees_ids"]:
            assignee = [u for u in users if u.id == int(assignee_id)]
            assignee = getUserData(assignee)
            expense["assignees"].append(assignee[0])
        if expense["open_user_id"] != None:
            open_user = [u for u in users if u.id == expense["open_user_id"]]
            open_user = getUserData(open_user)
            expense["open_user"] = open_user[0]
        if expense["processing_user_id"] != None:
            processing_user = [u for u in users if u.id == expense["processing_user_id"]]
            processing_user = getUserData(processing_user)
            expense["processing_user"] = processing_user[0]
        if expense["approve_user_id"] != None:
            approve_user = [u for u in users if u.id == expense["approve_user_id"]]
            approve_user = getUserData(approve_user)
            expense["approve_user"] = approve_user[0]
        if expense["reimburse_user_id"] != None:
            reimburse_user = [u for u in users if u.id == expense["reimburse_user_id"]]
            reimburse_user = getUserData(reimburse_user)
            expense["reimburse_user"] = reimburse_user[0]

        expensesData.append(expense)

    return expensesData

def toInt(variable):
    try:
        return int(variable)
    except:
        return None


def getReportIdsForAssignee(assignee, status):
    totalForReport = []
    if status != None:
        totalForReport = Expenses.objects.filter(
            Q(status=status),
            (Q(assignees=assignee) | Q(assignees__startswith=assignee + ",") | Q(assignees__endswith="," + assignee) | Q(assignees__contains="," + assignee + ",") 
            | Q(open_user_id=assignee) | Q(processing_user_id=assignee) | Q(approve_user_id=assignee) | Q(reimburse_user_id=assignee))).values(
            'report_id').distinct()
    else:
        totalForReport = Expenses.objects.filter(
            Q(status__gt=0),
            (Q(assignees=assignee) | Q(assignees__startswith=assignee + ",") | Q(assignees__endswith="," + assignee) | Q(assignees__contains="," + assignee + ",")
            | Q(open_user_id=assignee) | Q(processing_user_id=assignee) | Q(approve_user_id=assignee) | Q(reimburse_user_id=assignee))).values(
            'report_id').distinct()

    return totalForReport

def getCountForStatus(assignee, status):
    countData = Expenses.objects.filter(
            Q(status=status),
            (Q(assignees=assignee) | Q(assignees__startswith=assignee + ",") | Q(assignees__endswith="," + assignee) | Q(assignees__contains="," + assignee + ",")
            | Q(open_user_id=assignee) | Q(processing_user_id=assignee) | Q(approve_user_id=assignee) | Q(reimburse_user_id=assignee))).values(
            'company_id').annotate(count=Count('id'))
        
    if len(countData) == 0:
        return 0

    return countData[0]["count"]

def getTotalForReports(ids, assignee = None, status = None):
    totalForReport = []
    if assignee != None:
        if status != None:
            totalForReport = Expenses.objects.filter(
            Q(report_id__in=ids),
            Q(status=status),
            (Q(assignees=assignee) | Q(assignees__startswith=assignee + ",") | Q(assignees__endswith="," + assignee) | Q(assignees__contains="," + assignee + ",")
            | Q(open_user_id=assignee) | Q(processing_user_id=assignee) | Q(approve_user_id=assignee) | Q(reimburse_user_id=assignee))).values(
            'report_id', 
            'currency_type').annotate(total_amount=Sum('total_amount'), count=Count('id'))
        else:
            totalForReport = Expenses.objects.filter(
            Q(report_id__in=ids),
            Q(status__gt=0),
            (Q(assignees=assignee) | Q(assignees__startswith=assignee + ",") | Q(assignees__endswith="," + assignee) | Q(assignees__contains="," + assignee + ",")
            | Q(open_user_id=assignee) | Q(processing_user_id=assignee) | Q(approve_user_id=assignee) | Q(reimburse_user_id=assignee))).values(
            'report_id', 
            'currency_type').annotate(total_amount=Sum('total_amount'), count=Count('id'))
        
        return totalForReport
    else:
        totalForReport = Expenses.objects.filter(
            Q(status__gt=0),
            Q(report_id__in=ids)).values(
            'report_id', 
            'currency_type').annotate(total_amount=Sum('total_amount'))
        
        countForReport = Expenses.objects.filter(
            Q(report_id__in=ids)).values(
            'report_id', 
            'currency_type').annotate(count=Count('id'))

        ret = []
        for oCount in countForReport:
            oCount.__setitem__("total_amount", 0)
            for total in totalForReport:
                if oCount["report_id"] == total["report_id"] and oCount["currency_type"] == total["currency_type"]:
                    oCount["total_amount"] = total["total_amount"]
                    break

            ret.append(oCount)
        
        return ret

def getUsersWithIds(ids):
    users = Users.objects.filter(Q(id__in=ids))
    return users


def getReportData(reports):
    user_ids = []
    for report in reports:
        user_ids.append(report.user_id)
    
    users = getUsersWithIds(user_ids)
    reportsData = []
    for report in reports:
        user = [u for u in users if u.id == report.user_id]
        user = getUserData(user)
        reportData = {
            "id": report.id,
            "comment": report.comment,
            "payments_currency": report.payments_currency,
            "created_at": report.created_at,
            "updated_at": report.updated_at,
            "user": user[0]
        }
        reportsData.append(reportData)
    
    return reportsData

def getIndustryData(industryList):
    industries_data = []

    for industry in industryList:
        industry_data = {
            "id": industry.industry_id,
            "name": industry.name,
        }
        industries_data.append(industry_data)

    return industries_data


def getCountryData(countryList):
    countries_data = []

    for country in countryList:
        countryCode = Countries.objects.get(id=country.country_id)
        if countryCode is None:
            code = ''
        else:
            code = countryCode.code
        country_data = {
            "id": country.country_id,
            "code": code,
            "name": country.name,
        }
        countries_data.append(country_data)

    return countries_data


def getUserData(users):
    users_data = []

    for user in users:
        user_data = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "phone": user.phone,
            "job_title": user.job_title,
            "department": user.department,
            "language": user.language,
            "role_id": user.role_id,
            "avatar_url": user.avatar,
            "company_id": user.company_id,
            "reimbursement_cycle": user.reimbursement_cycle,
            "payments_currency": user.payments_currency
        }
        users_data.append(user_data)

    return users_data


def getUserDataWithPW(users):
    users_data = []

    for user in users:
        user_data = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "password": user.reset_password_token,
            "phone": user.phone,
            "job_title": user.job_title,
            "department": user.department,
            "language": user.language,
            "role_id": user.role_id,
            "avatar_url": user.avatar,
            "company_id": user.company_id,
            "reimbursement_cycle": user.reimbursement_cycle,
            "payments_currency": user.payments_currency
        }
        users_data.append(user_data)

    return users_data


def getExpenseDetail(expenses):
    expenses_data = []

    for expense in expenses:
        expense_data = {
            "id": expense.id,
            "merchant_name": expense.merchant_name,
            "receipt_date": expense.receipt_date,
            "description": expense.description,
            "total_amount": expense.total_amount,
            "category": expense.category,
            "assignees": expense.assignees,
            "file_urls": expense.file_urls,
            "file_names": expense.file_names,
            "user_id": expense.user_id,
            "open_user_id": expense.open_user_id,
            "processing_user_id": expense.processing_user_id,
            "approve_user_id": expense.approve_user_id,
            "reimburse_user_id": expense.reimburse_user_id,
            "company_id": expense.company_id,
            "report_id": expense.report_id,
            "status": expense.status,
            "payments_currency": expense.payments_currency,
            "currency_type": expense.currency_type,
            "created_at": expense.created_at,
            "updated_at": expense.updated_at,
        }
        expenses_data.append(expense_data)

    return expenses_data


def getReportDetail(reports):
    reports_data = []
    for report in reports:
        user = Users.objects.get(id=report.user_id)
        report_data = {
            "id": report.id,
            "comment": report.comment,
            "user": {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "job_title": user.job_title,
            },
            "created_at": report.created_at,
            "updated_at": report.updated_at,
        }
        reports_data.append(report_data)

    return reports_data


def getCompanyData(companies, lang):
    companies_data = []

    for company in companies:
        industryLocal = Industry_locales.objects.filter(language__startswith=lang,
                                                        industry_id=company.industry.id).first()
        countryLocal = Country_locales.objects.filter(language__startswith=lang, country_id=company.country.id).first()

        company_data = {
            "id": company.id,
            "name": company.name,
            "active_employees": company.active_employees,
            "total_expenses": company.total_expenses,
            "manage": company.manage,
            "website": company.website,
            "employee_count_index": company.employee_count_index,
            "created_at": company.created_at,
            "industry_id": company.industry_id,
            "country_id": company.country_id,
            "user_id": company.user_id,
            "industry": {
                "id": company.industry.id,
                "name": industryLocal.name
            },
            "country": {
                "id": company.country.id,
                "name": countryLocal.name
            }
        }
        companies_data.append(company_data)

    return companies_data

def uploadImage(userId, imageInfo):
    try:
        image = Images.objects.get(user_id=userId)
        image_serializer = ImageSerializer(image, data=imageInfo)
    except Images.DoesNotExist:
        image_serializer = ImageSerializer(data=imageInfo)

    if image_serializer.is_valid():
        image_serializer.save()

    return image_serializer

def exchangeMoney(money, fromNum, toNum):
    money = float(money)
    fromNum = int(fromNum)
    toNum = int(toNum)

    today = datetime.date.today()
    if constants.g_today != today:
        constants.g_utc = RealTimeCurrencyExchangeRate("USD", "CNY", constants.api_key)
        constants.g_etc = RealTimeCurrencyExchangeRate("EUR", "CNY", constants.api_key)
        constants.g_ctu = RealTimeCurrencyExchangeRate("CNY", "USD", constants.api_key)
        constants.g_etu = RealTimeCurrencyExchangeRate("EUR", "USD", constants.api_key)
        constants.g_ute = RealTimeCurrencyExchangeRate("USD", "EUR", constants.api_key)
        constants.g_cte = RealTimeCurrencyExchangeRate("CNY", "EUR", constants.api_key)
        constants.g_today = today

    if fromNum == toNum:
        money = money
    elif fromNum == 1 and toNum == 2:
        money = money * constants.g_ute
    elif fromNum == 1 and toNum == 3:
        money = money * constants.g_utc
    elif fromNum == 2 and toNum == 1:
        money = money * constants.g_etu
    elif fromNum == 2 and toNum == 3:
        money = money * constants.g_etc
    elif fromNum == 3 and toNum == 1:
        money = money * constants.g_ctu
    elif fromNum == 3 and toNum == 2:
        money = money * constants.g_cte

    return money


def RealTimeCurrencyExchangeRate(from_currency, to_currency, api_key):

    # base_url variable store base url
    base_url = r"https://api.exchangerate-api.com/v4/latest/"

    # main_url variable store complete url
    main_url = base_url + from_currency
    
    # get method of requests module
    # return response object
    req_ob = requests.get(main_url)

    # json method return json format
    # data into python dictionary data type.

    # result contains list of nested dictionaries
    result = req_ob.json()
    return float(result.get('rates').get(to_currency))
