from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from blog_api.models import Post
from blog_api.pagination import PostsPagination
from blog_api.serializers import ProfileSerializer, PostSerializer, AuthTokenSerializer
import django_filters

class GetProfile(APIView):
    def get(self, request, *args, **kwargs):
        return Response(ProfileSerializer(request.user).data)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class CreateProfile(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    Here the list of users
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'body')
    pagination_class = PostsPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @list_route(methods=['get'], url_path='my')
    def my_posts(self, request):
        """
        List of current user's posts
        """
        queryset = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
