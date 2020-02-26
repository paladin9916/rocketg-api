from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.api_view.utility import getCompanyData, getUserData
from apis.models import Companies, Users

from django.utils import translation


@api_view(['GET', 'POST'])
def componyGetSave(request):
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
        page_str = request.query_params.get('page')
        perPage_str = request.query_params.get('per_page')

        if page_str is None or page_str == '':
            page = 0
        else:
            page = int(page_str)

        if perPage_str is None or perPage_str == '':
            perPage = 10
        else:
            perPage = int(perPage_str)

        companyList = None
        try:
            companyList = Companies.objects.all().order_by('created_at')
        except Companies.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in getting company.')]}, status=status.HTTP_200_OK)

        total_count = companyList.count()
        paginator = Paginator(companyList, perPage)  # Show users per page

        try:
            companies = paginator.get_page(page + 1)
        except PageNotAnInteger:
            companies = paginator.page(1)
        except EmptyPage:
            companies = paginator.page(paginator.num_pages)

        companyData = getCompanyData(companies, lang)
        return Response(data={'success': True, 'data': companyData, 'totalRowCount': total_count}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get('name')
        website = request.data.get('website')
        employee_count_index = request.data.get('employee_count_index')
        user_id = request.data.get('user_id')
        country_id = request.data.get('country_id')
        industry_id = request.data.get('industry_id')
        company = Companies(name=name, website=website, employee_count_index=employee_count_index, user_id=user_id, country_id=country_id, industry_id=industry_id)

        try:
            company.save()
        except Companies.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in creating company.')]}, status=status.HTTP_200_OK)
        companyData = getCompanyData([company, ], lang)
        return Response(data={'success': True, 'data': companyData}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def componyUpdate(request, pk):
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

    if request.method == 'PUT':
        try:
            company = Companies.objects.get(pk=pk)
        except Companies.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Company do not exist.')]},
                            status=status.HTTP_200_OK)

        name = request.data.get('name')
        website = request.data.get('website')
        employee_count_index = request.data.get('employee_count_index')
        country_id = request.data.get('country_id')
        industry_id = request.data.get('industry_id')
        manage = request.data.get('manage')
        total_expenses = request.data.get('total_expenses')
        active_employees = request.data.get('active_employees')

        company.name = name
        company.website = website
        company.employee_count_index = employee_count_index
        company.country_id = country_id
        company.industry_id = industry_id
        company.manage = manage
        company.total_expenses = total_expenses
        company.active_employees = active_employees

        try:
            company.save()
        except Companies.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in updating company.')]}, status=status.HTTP_200_OK)
        companyData = getCompanyData([company, ], lang)
        return Response(data={'success': True, 'data': companyData}, status=status.HTTP_200_OK)

@api_view(['PUT', 'GET'])
def specialUsers(request, pk):
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

    companyId = pk
    company = None
    try:
        company = Companies.objects.get(pk=pk)
    except Companies.DoesNotExist:
        return Response(data={'success': False, 'error': [translation.gettext('Company do not exist.')]},
                        status=status.HTTP_200_OK)

    if request.method == 'PUT':
        openUserId = request.data.get('open')
        processingUserId = request.data.get('processing')
        approveUserId = request.data.get('approve')
        reimburseUserId = request.data.get('reimburse')

        company.open_user_id = openUserId
        company.processing_user_id = processingUserId
        company.approve_user_id = approveUserId
        company.reimburse_user_id = reimburseUserId
        
        try:
            company.save()
        except Companies.DoesNotExist:
            return Response(data={'success': False, 'error': [translation.gettext('Error in updating company.')]}, status=status.HTTP_200_OK)
        companyData = getCompanyData([company, ], lang)
        return Response(data={'success': True, 'data': companyData}, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        userIds = []
        if company.open_user_id != None:
            userIds.append(company.open_user_id)
        if company.processing_user_id != None:
            userIds.append(company.processing_user_id)
        if company.approve_user_id != None:
            userIds.append(company.approve_user_id)
        if company.reimburse_user_id != None:
            userIds.append(company.reimburse_user_id)        

        users = Users.objects.filter(Q(id__in=userIds), Q(company_id=companyId))
        userData = getUserData(users)

        data = {}
        for user in userData:
            if user["id"] == company.open_user_id:
                data["open"] = user
            if user["id"] == company.processing_user_id:
                data["processing"] = user
            if user["id"] == company.approve_user_id:
                data["approve"] = user
            if user["id"] == company.reimburse_user_id:
                data["reimburse"] = user
        
        return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def specialUser(request, pk, privilege):
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

    companyId = pk
    company = None
    try:
        company = Companies.objects.get(pk=pk)
    except Companies.DoesNotExist:
        return Response(data={'success': False, 'error': [translation.gettext('Company do not exist.')]},
                        status=status.HTTP_200_OK)

    users = None
    if privilege == 'open':
        users = Users.objects.filter(Q(id=company.open_user_id), Q(company_id=companyId))
    elif privilege == 'processing':
        users = Users.objects.filter(Q(id=company.processing_user_id), Q(company_id=companyId))
    elif privilege == 'approve':
        users = Users.objects.filter(Q(id=company.approve_user_id), Q(company_id=companyId))
    elif privilege == 'reimburse':
        users = Users.objects.filter(Q(id=company.reimburse_user_id), Q(company_id=companyId))

    userData = getUserData(users)
    
    return Response(data={'success': True, 'data': userData}, status=status.HTTP_200_OK)
