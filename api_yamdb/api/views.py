import re

from http import HTTPStatus

from django.db import IntegrityError

from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

#from .permissions import IsOwnerOrReadOnly
from titles.models import Category, Genre, GenreTitle, Title, Review, Comment
from .permissions import IsAdminRoleOrStaff
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, ReviewSerializer, CommentSerializer)

#  EXTRACT_POST_ID_PATTERN = r'posts\/([0-9]+)'

'''Заглушки viewsets'''


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,) #(IsAdminRoleOrStaff,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,) #(IsAdminRoleOrStaff ,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = StandardResultsSetPagination


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
