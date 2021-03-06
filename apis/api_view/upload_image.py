from random import randint
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from time import gmtime
from calendar import timegm

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apis.api_view.utility import uploadImage, isLoginUser
from apis.models import Users


class ImageUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['avatar']
        
        filePath = ''
        isSet = False
        for i in range(0, 30):
            filePath = str(randint(100000, 999999)) + str(timegm(gmtime()))
            if uploaded_file.name.lower().endswith('.jpg') or uploaded_file.name.lower().endswith('.jpeg'):
                filePath = filePath + ".jpg"
            elif uploaded_file.name.lower().endswith('.png'):
                filePath = filePath + ".png"

            fs = FileSystemStorage()
            if  fs.exists(filePath) == False:
                isSet = True
                break
        
        if isSet == False:
            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        fs.save(filePath, uploaded_file)

        return Response(data={'code': 0, 'success': True, 'data': {'avatar': settings.MEDIA_URL + filePath}}, status=status.HTTP_200_OK)
