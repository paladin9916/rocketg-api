from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apis.api_view.utility import uploadImage


class ImageUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        userId = request.data.get('user_id')
        if userId == '' or userId is None:
            userId = 0

        imageSerializer = uploadImage(userId, request.data)
        if imageSerializer.is_valid():
            return Response(imageSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(imageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
