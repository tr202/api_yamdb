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

from .permissions import IsOwnerOrReadOnly, IsAdminModeratorOwnerOrReadOnly
from titles.models import Category, Genre, GenreTitle, Title, Review, Comment
from .permissions import IsAdminRoleOrStaff
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, ReviewSerializer, CommentSerializer)

EXTRACT_TITLE_ID_PATTERN = r'titles\/([0-9]+)'


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
    search_fields = ('=category', '=genre', '=name', '=year')

    def create(self, request, *args, **kwargs):
        genres = Genre.objects.filter(slug__in=request.data.pop('genre', []))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer, genres)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=HTTPStatus.CREATED, headers=headers)
        except IntegrityError:
            return Response('Already exists', HTTPStatus.BAD_REQUEST)

    def perform_create(self, serializer, genre):
        serializer.save(genre=genre)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_title_id(self):
        pattern = EXTRACT_TITLE_ID_PATTERN
        return re.findall(pattern, self.request.path)[0]

    def get_queryset(self):
        return Review.objects.filter(
            title=self.get_title_id())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            title = Title.objects.get(pk=self.get_title_id())
            self.perform_create(serializer, title)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=HTTPStatus.CREATED, headers=headers)
        except IntegrityError:
            return Response('Already exists', HTTPStatus.BAD_REQUEST)

    def perform_create(self, serializer, title):
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
