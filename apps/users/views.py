import logging

from django.http import JsonResponse
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers import UserSerializers
from apps.utils import api_error
from apps.utils.data_serializer import SerializerUtils
from apps.utils.obj_response import ObjectResp

logger = logging.getLogger('apps')


class UserApiview(APIView):
    @api_error.handle_api_error
    def get(self, request):
        instance = User.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        arr_data = SerializerUtils(instance, page, page_size).paging_fun()
        ser = UserSerializers(instance=arr_data, many=True)
        data = ser.data
        response_dict = ObjectResp.response(code=200, message='success', ls=data)
        return JsonResponse(response_dict)

    @api_error.handle_api_error
    def post(self, request):
        pass
