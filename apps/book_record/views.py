import logging

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView

from apps.book_record.models import BookRecord
from apps.book_record.serializers import BookRecordShowSerializers, BookBorrowSerializers
from apps.books.models import Book
from apps.utils.data_serializer import SerializerUtils
from apps.utils.obj_response import ObjectResp

logger = logging.getLogger('apps')


class BookRecordApiview(APIView):
    def get(self, request):
        instance = BookRecord.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        arr_data = SerializerUtils(instance, page, page_size).paging_fun()
        ser = BookRecordShowSerializers(instance=arr_data, many=True)
        data = ser.data
        response_dict = ObjectResp.response(code=200, message='success', ls=data)
        return JsonResponse(response_dict)


class BookBorrowView(APIView):
    """借书接口"""

    def post(self, request):
        data = request.data
        ser = BookBorrowSerializers(data=data, context={'request': request})
        if not ser.is_valid():
            return JsonResponse(
                ObjectResp.response(code=400, message='数据验证失败', details=ser.errors),
                status=400
            )
        instance = ser.save()
        book_id = instance.book_id
        Book.objects.filter(id=book_id).update(status=2)
        return JsonResponse(ObjectResp.response(code=201, message='success'))


class BookReturnView(APIView):
    """还书接口"""

    def patch(self, request, record_id):
        try:
            record = BookRecord.objects.get(id=record_id, status=1)
            record.return_date = timezone.now().date()
            record.status = 2
            record.save()
            book_instance = Book.objects.get(id=record.book_id)
            if book_instance.status != 2:
                return JsonResponse(
                    ObjectResp.response(code=400, message='error', details='书籍状态错误'),
                    status=400
                )
            book_instance.status = 1
            book_instance.save()
            return JsonResponse(ObjectResp.response(code=200, message='success'))
        except BookRecord.DoesNotExist:
            return JsonResponse(
                ObjectResp.response(code=404, message='error', details='借阅记录不存在或已归还'),
                status=400
            )
        except Book.DoesNotExist:
            return JsonResponse(
                ObjectResp.response(code=404, message='error', details='图书不存在或已销毁'),
                status=400
            )
        except Exception as e:
            logger.exception("Internal Server Error")
            return JsonResponse(
                ObjectResp.response(code=500, message="服务器内部错误"),
                status=500
            )


