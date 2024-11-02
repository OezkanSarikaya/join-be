# from rest_framework import generics
# from user_auth_app.models import UserProfile
from .serializers import RegistrationSerializer #, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from join_api.models import Contact

# class UserProfileList(generics.ListCreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer

# class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
            }
        else:
            data=serializer.errors

        return Response(data)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            try:
                contact = Contact.objects.get(user=user)  # Hier user auf user_id prüfen, falls das Feld so heißt
                contact_data = contact.name
                
          
            except Contact.DoesNotExist:
                contact_data = None  # Falls kein Contact-Eintrag existiert


            data = {
                'token': token.key,
                'name': contact_data,
                'email': user.email,
            }
        else:
            data=serializer.errors

        return Response(data)
