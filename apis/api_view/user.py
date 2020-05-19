from django.contrib.auth.hashers import make_password
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apis.api_view import constants

from RocketG_api import settings
from apis.api_view.utility import getUserData, uploadImage, getUserDataWithPW, isLoginUser
from apis.models import Users, Companies

from django.utils import translation


@api_view(['GET', 'POST'])
def userGetSave(request):
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
            userList = Users.objects
            if request.query_params.get('company_id') != None:
                companyId = int(request.query_params.get('company_id'))
                userList = userList.filter(Q(company_id=companyId))
            
            if searchKey != None:
                userList = userList.filter(Q(email__contains=searchKey) | Q(firstname__contains=searchKey) | Q(
                                                lastname__contains=searchKey)).order_by('id')
        except Users.DoesNotExist:
            return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Error in getting user.')]}, status=status.HTTP_200_OK)

        total_count = userList.count()
        paginator = Paginator(userList, perPage)  # Show users per page

        try:
            users = paginator.get_page(page + 1)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        userData = getUserData(users)
        return Response(data={'code': 0, 'success': True, 'data': userData, 'totalRowCount': total_count},
                        status=status.HTTP_200_OK)
    elif request.method == 'POST':
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        jobTitle = request.POST.get('job_title')
        department = request.POST.get('department')
        language = request.POST.get('language')
        roleId = int(request.POST.get('role_id'))
        companyId = int(request.POST.get('company_id'))
        reporterId = request.POST.get('reporter_id')
        avatar = request.POST.get('avatar')
        reimbursementCycle = int(request.POST.get('reimbursement_cycle'))
        paymentsCurrency = request.POST.get('payments_currency')

        if paymentsCurrency in constants.g_currency_keys:
            None
        else:
            return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Error in creating User.')]},
                                    status=status.HTTP_200_OK)

        if reporterId != None:
            reporterId = int(reporterId)

        try:
            if Users.objects.get(email=email):
                return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Exist this email. Please try again.')]},
                                status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            try:
                if Users.objects.get(phone=phone):
                    return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Exist this phone number. Please try again.')]},
                                    status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                password = get_random_string(length=16)
                salt = settings.SECRET_KEY
                encryptedPassword = make_password(password, salt=salt)

                user = Users(uid=email, email=email, firstname=firstname, lastname=lastname,
                             encrypted_password=encryptedPassword, reset_password_token=password, phone=phone,
                             job_title=jobTitle, avatar=avatar, reporter_id=reporterId,
                             department=department, language=language, role_id=roleId, company_id=companyId,
                             reimbursement_cycle=reimbursementCycle, payments_currency=paymentsCurrency)

                try:
                    user.save()
                    company = Companies.objects.get(id=companyId)
                    company.active_employees += 1
                    company.save()
                except Users.DoesNotExist:
                    return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Error in creating User.')]},
                                    status=status.HTTP_200_OK)
                user.save()

                userData = getUserDataWithPW([user, ])
                return Response(data={'code': 0, 'success': True, 'data': userData}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
def userDetailUpdate(request, pk):
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

    try:
        user = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('User do not exist.')]},
                        status=status.HTTP_200_OK)

    if request.method == 'GET':
        userData = getUserData([user, ])
        return Response(data={'code': 0, 'success': True, 'data': userData}, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        email = request.POST.get('email')
        # password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        jobTitle = request.POST.get('job_title')
        department = request.POST.get('department')
        language = request.POST.get('language')
        roleId = int(request.POST.get('role_id'))
        companyId = int(request.POST.get('company_id'))
        reporterId = request.POST.get('reporter_id')
        avatar = request.POST.get('avatar')
        reimbursementCycle = int(request.POST.get('reimbursement_cycle'))
        paymentsCurrency = request.POST.get('payments_currency')

        if paymentsCurrency in constants.g_currency_keys:
            None
        else:
            return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Error in updating user.')]},
                                    status=status.HTTP_200_OK)

        if reporterId != None:
            reporterId = int(reporterId)

        try:
            if Users.objects.get(~Q(id=pk), Q(email=email)):
                return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Exist this email. Please try again.')]},
                                status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            try:
                if Users.objects.get(~Q(id=pk), Q(phone=phone)):
                    return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Exist this phone number. Please try again.')]},
                                    status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                if (user.avatar != None and avatar == None) or (user.avatar != None and user.avatar.strip() != avatar.strip()):
                    filePath = str(user.avatar)
                    filePath = filePath.replace("/media/", "")

                    if len(filePath) > 0:
                        fs = FileSystemStorage()
                        fs.delete(filePath)

                user.uid = email
                user.email = email
                user.firstname = firstname
                user.lastname = lastname
                user.phone = phone
                user.job_title = jobTitle
                user.department = department
                user.language = language
                user.role_id = roleId
                user.company_id = companyId
                user.reporter_id = reporterId
                user.reimbursement_cycle = reimbursementCycle
                user.payments_currency = paymentsCurrency
                user.avatar = avatar

                try:
                    user.save()
                except Users.DoesNotExist:
                    return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Error in updating user.')]},
                                    status=status.HTTP_200_OK)

                userData = getUserData([user, ])
                return Response(data={'code': 0, 'success': True, 'data': userData}, status=status.HTTP_200_OK)


@api_view(['POST'])
def resetPassword(request):
    if request.method == 'POST':
        userId = request.POST.get('user_id')
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

        password = get_random_string(length=16)
        salt = settings.SECRET_KEY
        encryptedPassword = make_password(password, salt=salt)

        try:
            user = Users.objects.get(id=userId)
            user.reset_password_token = password
            user.encrypted_password = encryptedPassword
            user.save()
        except Users.DoesNotExist:
            return Response(data={'code': 2, 'success': False, 'error': [translation.gettext('Error in reseting password.')]},
                            status=status.HTTP_200_OK)

        return Response(data={'code': 0, 'success': True, 'data': {"password": password}}, status=status.HTTP_200_OK)
