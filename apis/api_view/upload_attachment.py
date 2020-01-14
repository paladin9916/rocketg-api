from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apis.api_view.utility import uploadExpenseFile
from apis.models import Expenses


class AttachmentUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        expenseId = request.data.get('expense_id')
        if expenseId == '' or expenseId is None:
            expenseId = 0

        fileSerializer = uploadExpenseFile(expenseId, request.data)
        if fileSerializer.is_valid():
            if expenseId != 0:
                expense = Expenses.objects.get(id=expenseId)
                expense.file_urls = fileName
                expense.file_names = fileName
                expense.save()
                
            return Response(fileSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
