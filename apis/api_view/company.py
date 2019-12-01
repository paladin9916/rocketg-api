from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.api_view.data_manage import getCompanyData
from apis.models import Companies


@api_view(['GET', 'POST'])
def componyGetSave(request):
    token = request.headers.get('access-token')
    client = request.headers.get('client')
    uid = request.headers.get('uid')
    lang = request.headers.get('lang')

    if lang is None or lang == '':
        lang = 'en'

    if request.method == 'GET':
        page = int(request.query_params.get('page'))
        perPage = int(request.query_params.get('per_page'))
        if perPage is None or perPage == 0:
            perPage = 10

        companyList = None
        try:
            companyList = Companies.objects.all().order_by('created_at')
        except Companies.DoesNotExist:
            return Response(data={'success': False, 'error': ['Error in getting company.']}, status=status.HTTP_200_OK)

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
            return Response(data={'success': False, 'error': ['Error in creating company.']}, status=status.HTTP_200_OK)
        companyData = getCompanyData([company, ], lang)
        return Response(data={'success': True, 'data': companyData}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def componyUpdate(request, pk):
    token = request.headers.get('access-token')
    client = request.headers.get('client')
    uid = request.headers.get('uid')
    lang = request.headers.get('lang')

    if request.method == 'PUT':
        try:
            company = Companies.objects.get(pk=pk)
        except Companies.DoesNotExist:
            return Response(data={'success': False, 'error': ['Company do not exist.']},
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
        company.save()

        try:
            company.save()
        except Companies.DoesNotExist:
            return Response(data={'success': False, 'error': ['Error in updating company.']}, status=status.HTTP_200_OK)
        companyData = getCompanyData([company, ], lang)
        return Response(data={'success': True, 'data': companyData}, status=status.HTTP_200_OK)