from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser


from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions




# expect function for differnt type request can be made to APIVIew
class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
            "Uses HTTP method as function(get, post, patch, put, delete)",
            "Is similar to Django View",
            "Gives you most control over your application logic",
            "Is mapped manually to URLs"
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('full_name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'mathod': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete object in the database"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Route',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message':message})
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle retrieve an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(Self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method' : 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
        """Handle creating and updating profiles"""
        serializer_class = serializers.UserProfileSerializer
        # recognize all the methods that we want to use while using serializer
        queryset = models.UserProfile.objects.all()
        authentication_classes = (TokenAuthentication,)
        permission_classes = (permissions.UpdateOwnProfile,)
        filter_backends = (filters.SearchFilter,)
        search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handle creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    parser_classes = (FormParser, MultiPartParser)

    queryset = models.ProfileFeedItem.objects.all()

    permission_classes = ( permissions.UpdateOwnStatus, IsAuthenticated)

    # customize the logic of creating an object. Called every time we go HTTP post to viewset
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        # file_uploaded = self.request.FILES.get('file_uploaded')
        file_name = serializer.validated_data['file_uploaded'] # access file

        # content_type = file_uploaded.content_type
        user_feed = serializer.save(user_profile=self.request.user)

        uploaded_file_location_dict = models.ProfileFeedItem.objects.filter(id=user_feed.id).only('file_uploaded').values()[0]
        uploaded_file_location = uploaded_file_location_dict.get("uploaded_file_location")
