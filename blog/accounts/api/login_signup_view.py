from accounts.models import User

from rest_framework import status, viewsets

from utils.global_utils import validate_fields, create_response
from blogapp.authentication import get_tokens_for_user

from accounts.serializer import UserProfileCreateSerializer

class SignupWithPassword(viewsets.ViewSet):

    def create(self, request):
        data = request.data

        try:

            user_name = data.get('username')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            mobile = data.get('mobile')
            country_code = data.get('country_code')
            email = data.get('email')
            password = data.get('password')

            validation_fields = {
                "User Name": {"value":user_name, "checks":['username']},
                "Full Name":{"value":f"{first_name or ''} {last_name or ''}".strip(), "checks":"full_name"},
                "Mobile":{"value":mobile, "checks":['mobile']},
                "Country Code":{"value":country_code, "checks":['country_code']},
                "E-mail":{"value":email, "checks":['email']},
                "Password":{"value":password, "checks":['password']}
            }

            response = validate_fields(validation_fields)

            if response:
                return create_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=response
                )
            
            serialized_user_obj = UserProfileCreateSerializer(data=data)
            if serialized_user_obj.is_valid():
                user = serialized_user_obj.save()
                token = get_tokens_for_user(user) 
            
            return create_response(
                message="User created Successfully",
                status=status.HTTP_201_CREATED, 
                result=token
            )
            
        except Exception as e:
            return create_response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Exception : {e}"
            )
        
class LoginWithPassword(viewsets.ViewSet):
    def create(self, request):
        try:
            mobile = request.data.get("mobile")
            country_code = request.data.get("country_code")
            password = request.data.get("password")

            user_obj = User.objects.get(mobile=mobile, country_code=country_code, is_deleted=False)
            if not user_obj:
                return create_response(
                    status=status.HTTP_404_NOT_FOUND,
                    message="User not found"
                )
            
            if user_obj.password != password:
                return create_response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    message="Invalid Password"
                )
            
            token = get_tokens_for_user(user_obj)
            
            return create_response(
                status=status.HTTP_200_OK,
                message="User Logged in Successfully",
                result=token
            )

        except Exception as e:
                return create_response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=f"Exception : {e}"
                )