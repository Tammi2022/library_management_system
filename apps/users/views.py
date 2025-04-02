import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers import UserSerializers
from apps.utils.data_serializer import SerializerUtils
from apps.utils.obj_response import ObjectResp

logger = logging.getLogger('apps')


class UserApiview(APIView):
    def get(self, request):
        instance = User.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        arr_data = SerializerUtils(instance, page, page_size).paging_fun()
        ser = UserSerializers(instance=arr_data, many=True)
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
            ser = UserSerializers(data=request.data)
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
            logger.exception("Internal Server Error")
            return JsonResponse(
                ObjectResp.response(code=500, message="服务器内部错误"),
                status=500
            )


class UserEditApiview(APIView):
    def put(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            ser = UserSerializers(
                instance=user,
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
