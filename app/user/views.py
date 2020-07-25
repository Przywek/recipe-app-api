from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSelializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """docstring for ."""
    serializer_class = UserSelializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    serializer_class = UserSelializer
    authentication_classes = (authentication.TokenAuthentication,)
    permissions = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and reurn authenticate user"""
        return self.request.user
