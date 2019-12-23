from django.contrib.auth.hashers import make_password
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from RocketG_api import settings
from apis.api_view.utility import getUserData, uploadImage, getUserDataWithPW
from apis.models import Users, Companies


@api_view(['GET', 'POST'])
def userGetSave(request):
    token = request.headers.get('access-token')
    client = request.headers.get('client')
    uid = request.headers.get('uid')
    lang = request.headers.get('lang')

    if lang is None or lang == '':
        lang = 'en'

    if request.method == 'GET':
        page_str = request.query_params.get('page')
        perPage_str = request.query_params.get('per_page')
        companyId = int(request.query_params.get('company_id'))
        searchKey = request.query_params.get('search_key')

        if page_str is None or page_str == '':
            page = 0
        else:
            page = int(page_str)

        if perPage_str is None or perPage_str == '':
            perPage = 10
        else:
            perPage = int(perPage_str)

        userList = None
        try:
            userList = Users.objects.filter(Q(company_id=companyId),
                                            Q(email__contains=searchKey) | Q(firstname__contains=searchKey) | Q(
                                                lastname__contains=searchKey)).order_by('id')
        except Users.DoesNotExist:
            return Response(data={'success': False, 'error': ['Error in getting user.']}, status=status.HTTP_200_OK)

        total_count = userList.count()
        paginator = Paginator(userList, perPage)  # Show users per page

        try:
            users = paginator.get_page(page + 1)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        userData = getUserData(users)
        return Response(data={'success': True, 'data': userData, 'totalRowCount': total_count},
                        status=status.HTTP_200_OK)
    elif request.method == 'POST':
        email = request.data.get('email')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        phone = request.data.get('phone')
        jobTitle = request.data.get('job_title')
        department = request.data.get('department')
        language = request.data.get('language')
        roleId = request.data.get('role_id')
        companyId = request.data.get('company_id')
        avatar = request.data.get('avatar')
        reimbursementCycle = request.data.get('reimbursement_cycle')
        paymentsCurrency = request.data.get('payments_currency')

        try:
            if Users.objects.get(email=email):
                return Response(data={'success': False, 'error': ['Exist this email. Please try again.']},
                                status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            try:
                if Users.objects.get(phone=phone):
                    return Response(data={'success': False, 'error': ['Exist this phone number. Please try again.']},
                                    status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                password = get_random_string(length=16)
                salt = settings.SECRET_KEY
                encryptedPassword = make_password(password, salt=salt)

                user = Users(uid=email, email=email, firstname=firstname, lastname=lastname, encrypted_password=encryptedPassword, reset_password_token=password, phone=phone, job_title=jobTitle,
                             department=department, language=language, role_id=roleId, company_id=companyId,
                             reimbursement_cycle=reimbursementCycle, payments_currency=paymentsCurrency)

                try:
                    user.save()
                    company = Companies.objects.get(id=companyId)
                    company.active_employees += 1
                    company.save()
                except Users.DoesNotExist:
                    return Response(data={'success': False, 'error': ['Error in creating User.']}, status=status.HTTP_200_OK)

                # upload avatar
                imageSerData = {
                    "user_id": user.id,
                    "avatar": avatar
                }
                imageSerializer = uploadImage(user.id, imageSerData)
                user.avatar = imageSerializer.data.get('avatar')
                user.save()

                userData = getUserDataWithPW([user, ])
                return Response(data={'success': True, 'data': userData}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
def userDetailUpdate(request, pk):
    token = request.headers.get('access-token')
    client = request.headers.get('client')
    uid = request.headers.get('uid')
    lang = request.headers.get('lang')

    try:
        user = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(data={'success': False, 'error': ['User do not exist.']},
                        status=status.HTTP_200_OK)

    if request.method == 'GET':
        userData = getUserData([user, ])
        return Response(data={'success': True, 'data': userData}, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        email = request.data.get('email')
        # password = request.data.get('password')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        phone = request.data.get('phone')
        jobTitle = request.data.get('job_title')
        department = request.data.get('department')
        language = request.data.get('language')
        roleId = request.data.get('role_id')
        companyId = request.data.get('company_id')
        avatar = request.data.get('avatar')
        reimbursementCycle = request.data.get('reimbursement_cycle')
        paymentsCurrency = request.data.get('payments_currency')

        try:
            if Users.objects.get(email=email):
                return Response(data={'success': False, 'error': ['Exist this email. Please try again.']},
                                status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            try:
                if Users.objects.get(phone=phone):
                    return Response(data={'success': False, 'error': ['Exist this phone number. Please try again.']},
                                    status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                user.email = email
                user.firstname = firstname
                user.lastname = lastname
                user.phone = phone
                user.job_title = jobTitle
                user.department = department
                user.language = language
                user.role_id = roleId
                user.company_id = companyId
                user.reimbursement_cycle = reimbursementCycle
                user.payments_currency = paymentsCurrency

                # upload avatar
                imageSerData = {
                    "user_id": pk,
                    "avatar": avatar
                }
                imageSerializer = uploadImage(pk, imageSerData)
                user.avatar = imageSerializer.data.get('avatar')

                try:
                    user.save()
                except Users.DoesNotExist:
                    return Response(data={'success': False, 'error': ['Error in updating user.']},
                                    status=status.HTTP_200_OK)

                userData = getUserData([user, ])
                return Response(data={'success': True, 'data': userData}, status=status.HTTP_200_OK)


@api_view(['POST'])
def resetPassword(request):
    if request.method == 'POST':
        userId = request.data.get('user_id')

        password = get_random_string(length=16)
        salt = settings.SECRET_KEY
        encryptedPassword = make_password(password, salt=salt)

        try:
           user = Users.objects.get(id=userId)
           user.reset_password_token = password
           user.encrypted_password = encryptedPassword
           user.save()
        except Users.DoesNotExist:
            return Response(data={'success': False, 'error': ['Error in reseting password.']}, status=status.HTTP_200_OK)

        return Response(data={'success': True, 'data': {"password": password}}, status=status.HTTP_200_OK)