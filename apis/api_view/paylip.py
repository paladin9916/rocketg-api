from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.api_view.utility import getPaylipData, isLoginUser
from apis.models import Users, Paylips

from django.utils import translation

@api_view(['GET'])
def myPaylips(request):
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
            
        me = login_user = Users.objects.get(email=uid)
        pays = Paylips.objects.filter(Q(user_id=me.id)).order_by('name')

        total_count = pays.count()
        paginator = Paginator(pays, perPage)  # Show users per page

        try:
            pays = paginator.get_page(page + 1)
        except PageNotAnInteger:
            pays = paginator.page(1)
        except EmptyPage:
            pays = paginator.page(paginator.num_pages)

        data = getPaylipData(pays)

        return Response(data={'code': 0, 'success': True, 'data': data, 'totalRowCount': total_count}, status=status.HTTP_200_OK)

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

    isLogin = isLoginUser(request)
    if isLogin == False:
        return Response(data={'code': 1, 'success': False, 'error': [translation.gettext('Your session expired, please log in.')]},
                        status=status.HTTP_200_OK)

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

        pays = Paylips.objects.filter(Q(user_id=user)).order_by('name')

        total_count = pays.count()
        paginator = Paginator(pays, perPage)  # Show users per page

        try:
            pays = paginator.get_page(page + 1)
        except PageNotAnInteger:
            pays = paginator.page(1)
        except EmptyPage:
            pays = paginator.page(paginator.num_pages)

        data = getPaylipData(pays)

        return Response(data={'code': 0, 'success': True, 'data': data, 'totalRowCount': total_count}, status=status.HTTP_200_OK)
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
            return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Error in creating company.')]}, status=status.HTTP_200_OK)

        return Response(data={'code': 0, 'success': True, 'data': 'success'}, status=status.HTTP_200_OK)
