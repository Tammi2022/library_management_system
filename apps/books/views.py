import logging

from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from apps.books.models import Book
from apps.books.serializers import BookSerializers
from apps.utils.data_serializer import SerializerUtils
from apps.utils.obj_response import ObjectResp

logger = logging.getLogger('apps')


class BookApiview(APIView):
    def get(self, request):
        instance = Book.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        arr_data = SerializerUtils(instance, page, page_size).paging_fun()
        ser = BookSerializers(instance=arr_data, many=True)
        data = ser.data
        response_dict = ObjectResp.response(code=200, message='success', ls=data)
        return JsonResponse(response_dict)

    def post(self, request):
        try:
            # 检查是否有请求数据
            if not request.data:
                logger.error("Request data is empty.")
                return JsonResponse(
                    ObjectResp.response(code=400, message="请求数据为空"),
                    status=400
                )
            ser = BookSerializers(data=request.data)
            if ser.is_valid():
                ser.save()
                return JsonResponse(ObjectResp.response(code=200, message='success'))
            else:
                # 明确记录验证错误细节
                logger.error(f"Validation Error: {ser.errors}")
                return JsonResponse(
                    ObjectResp.response(code=400, message='数据验证失败', details=ser.errors),
                    status=400
                )
        except Exception as e:
            logger.exception("Internal Server Error")
            return JsonResponse(
                ObjectResp.response(code=500, message="服务器内部错误"),
                status=500
            )


class BookEditApiview(APIView):
    def put(self, request, book_id):
        try:
            book = get_object_or_404(Book, id=book_id)
            ser = BookSerializers(
                instance=book,
                data=request.data
            )
            if ser.is_valid():
                ser.save()
                return JsonResponse(ObjectResp.response(code=200, message='success'))
            else:
                logger.error(f"Validation Error: {ser.errors}")
                return JsonResponse(
                    ObjectResp.response(code=400, message='数据验证失败', details=ser.errors),
                    status=400
                )
        except Exception as e:
            logger.exception("Full Update Error")
            return JsonResponse(
                ObjectResp.response(code=500, message="服务器内部错误"),
                status=500
            )


class BookDestructionApiview(APIView):

    def patch(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.status = 3
            book.save()
            return JsonResponse(ObjectResp.response(code=200, message='success'))
        except Book.DoesNotExist:
            return JsonResponse(
                ObjectResp.response(code=404, message='error', details='图书记录不存在'),
                status=400
            )
        except Exception as e:
            logger.exception("Internal Server Error")
            return JsonResponse(
                ObjectResp.response(code=500, message="服务器内部错误"),
                status=500
            )
