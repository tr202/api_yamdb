import json
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import YamdbUser
from .permissions import IsAdminRole
from .serializers import (FullYamdbUserSerialiser,
                          RestrictRoleYamdbUserSerialiser,
                          YamdbUserSerializer)
from .utils import confirmation_code_generator, send_confirm_email


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class YamdbUsersViewSet(viewsets.ModelViewSet):
    model = YamdbUser
    permission_classes = (IsAdminRole,)
    serializer_class = FullYamdbUserSerialiser
    queryset = YamdbUser.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    http_method_names = ('get', 'delete', 'post', 'patch',)
    pagination_class = StandardResultsSetPagination
    lookup_field = 'username'

    @action(detail=False, methods=('get', 'patch',), url_path='me',
            url_name='me', permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        self.serializer_class = RestrictRoleYamdbUserSerialiser
        self.lookup_field = 'pk'
        self.kwargs['pk'] = request.user.pk

        return (
            self.retrieve(request) if request.method == 'GET'
            else self.partial_update(request))


class SignupViewSet(CreateModelMixin, viewsets.GenericViewSet):
    model = YamdbUser
    permission_classes = (permissions.AllowAny,)
    serializer_class = YamdbUserSerializer
    queryset = YamdbUser.objects.all()

    def create(self, request, *args, **kwargs):
        self.conf_code = confirmation_code_generator()
        try:
            user = self.model.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
            user.set_password(self.conf_code) and user.save()
            send_confirm_email(self.conf_code, user.email)
            return Response('Already exists', status.HTTP_200_OK)
        except Exception:
            response = super().create(request, *args, **kwargs)
            send_confirm_email(self.conf_code, self.user.email)
            response.status_code = status.HTTP_200_OK
            return response

    def perform_create(self, serializer):
        self.user = serializer.save(password=self.conf_code)
