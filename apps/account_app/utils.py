from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


def get_tokens(user: CustomUser) -> dict[str, str]:
    access = AccessToken.for_user(user=user)
    refresh = RefreshToken.for_user(user=user)
    return {
        'refresh': str(refresh),
        'access': str(access),
    }


def validate_and_format_phone(phone_number: str) -> str | Exception:
    if len(phone_number) != 11:
        raise Exception('phone number must be 11 character')
    else:
        try:
            int(phone_number)
        except ValueError:
            raise Exception('phone number is invalid')
        return phone_number
