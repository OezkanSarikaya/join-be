from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile
# from django.contrib.auth import authenticate
from join_api.models import Contact

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs= {
            'password': {
                'write_only' : True
            }
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error':'passwords dont match'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'A user with this email already exists'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
 
        contact = Contact.objects.filter(user__isnull=True, email=email).first()
        if contact:
            contact.user = account  # Verknüpft den bestehenden Contact mit dem User
            contact.save()
        else:
            raise serializers.ValidationError({'error': 'Contact entry not found for this user'})      

        return account    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class LoginSerializer(serializers.ModelSerializer):
  

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'repeated_password']
#         extra_kwargs= {
#             'password': {
#                 'write_only' : True
#             }
#         }

   






