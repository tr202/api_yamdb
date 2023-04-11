import re

from http import HTTPStatus

from django.db import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from .permissions import IsOwnerOrReadOnly, IsAdminModeratorOwnerOrReadOnly, IsAdminRole
from reviews.models import Category, Genre, GenreTitle, Title, Review, Comment
from .permissions import IsAdminRoleOrStaff
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleDetailSerializer,
                          ReviewSerializer, CommentSerializer)

EXTRACT_TITLE_ID_PATTERN = r'titles\/([0-9]+)'
EXTRACT_TITLE_ID_AND_REVIEW_ID = r'titles\/([0-9]+)\/reviews\/([0-9]+)'
METHOD_NOT_ALLOWED = 'Method not allowed'


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500


class BaseCategoryGenreViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminRoleOrStaff,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(METHOD_NOT_ALLOWED, status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(METHOD_NOT_ALLOWED, status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(BaseCategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminRole,)
    queryset = Title.objects.all().select_related('category')
    serializer_class = TitleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=category', '=genre', '=name', '=year')

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TitleDetailSerializer
        return super(TitleViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        #_mutable = request.data
        request.data._mutable = True
        genres = Genre.objects.filter(slug__in=request.data.pop('genre', []))
        request.data._mutable = False
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
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_title_id(self):
        pattern = EXTRACT_TITLE_ID_PATTERN
        return re.findall(pattern, self.request.path)[0]

    def get_queryset(self):
        return Review.objects.filter(
            title=self.get_title_id())

    #def check_exists(self, title, user):
     #   return Review.objects.filter(title=title, author=user).exists()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            title = Title.objects.get(pk=self.get_title_id())
            #if self.check_exists(title, request.user):
             #   return Response('Already exists', status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer, title)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return Response('Already exists', status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, title):
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_ids(self):
        pattern = EXTRACT_TITLE_ID_AND_REVIEW_ID
        ids = re.findall(pattern, self.request.path)
        self.title_id = ids[0][0]
        self.review_id = ids[0][1]
        return True

    def get_queryset(self):
        self.get_ids()
        print(self.title_id, ' ', self.review_id)
        return Comment.objects.filter(review_id=self.review_id)
    
    def create(self, request, *args, **kwargs):
        self.get_ids()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            review = Review.objects.get(pk=self.review_id)
            self.perform_create(serializer, review)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return Response('Already exists', status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, review):
        serializer.save(author=self.request.user, review=review)
