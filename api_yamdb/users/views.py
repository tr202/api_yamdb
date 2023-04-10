from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import YamdbUser
from .permissions import IsAdminRole
from .serializers import (FullYamdbUserSerialiser,
                          YamdbUserSerializer,
                          RestrictRoleYamdbUserSerialiser)
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

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            url_name='me', permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        self.serializer_class = RestrictRoleYamdbUserSerialiser
        self.lookup_field = 'pk'
        self.kwargs['pk'] = request.user.pk

        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            return self.partial_update(request)
        else:
            raise Exception('Not implemented')


class SignupViewSet(CreateModelMixin, viewsets.GenericViewSet):
    model = YamdbUser
    permission_classes = (permissions.AllowAny,)
    serializer_class = YamdbUserSerializer
    queryset = YamdbUser.objects.all()
    # http_method_names = ['post']

    def check_exists(self, data):
        if data.get('username') and data.get('email'):
            username = data.get('username')
            email = data.get('email')
            try:
                user = self.model.objects.get(username=username, email=email)
                print(user)
                return user
            except ObjectDoesNotExist:
                print('not Exists')
                return False

    def create(self, request, *args, **kwargs):
        user = self.check_exists(request.data)
        confirmation_code = confirmation_code_generator()
        if user:
            user.set_password(confirmation_code)
            user.save()
            send_confirm_email(confirmation_code, user.email)
            return Response('Already exists', status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, confirmation_code)
        send_confirm_email(confirmation_code, request.data.get('email'))
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer, confirmation_code):
        serializer.save(password=confirmation_code)
