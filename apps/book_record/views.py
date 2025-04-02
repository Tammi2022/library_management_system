import logging

from django.http import JsonResponse
from rest_framework.views import APIView

from apps.book_record.serializers import BookRecordSerializers
from apps.books.models import Book
from apps.utils import api_error
from apps.utils.data_serializer import SerializerUtils
from apps.utils.obj_response import ObjectResp

logger = logging.getLogger('apps')


class BookRecordApiview(APIView):
    @api_error.handle_api_error
    def get(self, request):
        instance = Book.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        arr_data = SerializerUtils(instance, page, page_size).paging_fun()
        ser = BookRecordSerializers(instance=arr_data, many=True)
        data = ser.data
        response_dict = ObjectResp.response(code=200, message='success', ls=data)
        return JsonResponse(response_dict)

    @api_error.handle_api_error
    def post(self, request):
        pass
