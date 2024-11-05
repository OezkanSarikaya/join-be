from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import RegistrationSerializer, UserProfileSerializer #LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from join_api.models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status

def get_guest_user():
    guest_username = "guest@domain.com"
    
    # Gastbenutzer abrufen oder erstellen
    guest_user, created = User.objects.get_or_create(
        username=guest_username,
        defaults={'is_active': True, 'first_name': 'Guest','email': "guest@domain.com",}
    )
    
    if created:
        guest_user.set_unusable_password()  # Gast-Benutzer ohne Passwort
        guest_user.save()

    # Token für den Gastbenutzer abrufen oder erstellen
    token, _ = Token.objects.get_or_create(user=guest_user)
    
    # Kontakt für den Gastbenutzer abrufen oder erstellen
    Contact.objects.get_or_create(
        user=guest_user,
        defaults={
            'email': "guest@domain.com",  # Pseudo-Email für den Gast
            'name': "Guest User",
            'color': 0  # Beispielwert für Farbe, falls erforderlich
        }
    )
    
    return guest_user, token

class UserProfileList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

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


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        is_guest = request.data.get("is_guest", False)
        data = {}

        if is_guest:
            # Gastzugang gewähren
            guest_user, token = get_guest_user()
            data = {
                "token": token.key,
                "username": guest_user.username,
                "email": "guest@domain.com",  # Evtl. als Pseudoe-Mail für Gast
                "name": "Guest User"
            }
            return Response(data, status=status.HTTP_200_OK)

        email = request.data.get('email')
        password = request.data.get('password')
        # serializer = LoginSerializer(data=request.data)
        # data = {}

        # Überprüfen, ob die E-Mail im System existiert
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Email not registered'}, status=status.HTTP_200_OK)

        # Authentifizierung des Benutzers mit Passwort
        user = authenticate(request, username=user.username, password=password)
        if user is None:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_200_OK)

        # Falls Login erfolgreich, Token generieren und Contact-Daten abrufen
        token, created = Token.objects.get_or_create(user=user)

        try:
            contact = Contact.objects.get(user=user)
            contact_data = contact.name  # Beispiel, wenn nur der Name benötigt wird
        except Contact.DoesNotExist:
            contact_data = None

        data = {
            'token': token.key,
            'name': contact_data,
            'email': user.email,
        }
        return Response(data)