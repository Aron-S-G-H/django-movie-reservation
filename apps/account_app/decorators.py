from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializer import UserLoginSerializer, UserRegisterSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from utils.custom_decorator import custom_decorator


user_login_decorator = custom_decorator(
    request=UserLoginSerializer,
    responses={200: 'application/json'},
    methods=['POST'],
    summary='Obtain tokens for registered user',
    description='Obtain access token & refresh token for registered user along with users information',
    examples=[
        OpenApiExample(
            response_only=True,
            name='Successful login response',
            status_codes=["200"],
            value={
                'access': 'string',
                'refresh': 'string',
                'user': {
                    "id": 0,
                    "last_login": "2024-10-30T22:47:28.276Z",
                    "is_superuser": True,
                    "first_name": "string",
                    "last_name": "string",
                    "is_staff": True,
                    "is_active": True,
                    "date_joined": "2024-10-30T22:47:28.276Z",
                    "email": "user@example.com",
                    "phone": "string"
                }
            }
        ),
    ],
    url_path='login',
    detail=False,
    url_name='login',
)

user_register_decorator = custom_decorator(
    request=UserRegisterSerializer,
    responses={201: 'application/json'},
    methods=['POST'],
    summary='Register a user and obtain tokens',
    description='Register a new user and obtain access & refresh token along with user information',
    examples=[
        OpenApiExample(
            response_only=True,
            name='Successful register response',
            status_codes=["201"],
            value={
                'access': 'string',
                'refresh': 'string',
                'user': {
                    "id": 0,
                    "last_login": "2024-10-30T22:47:28.276Z",
                    "is_superuser": True,
                    "first_name": "string",
                    "last_name": "string",
                    "is_staff": True,
                    "is_active": True,
                    "date_joined": "2024-10-30T22:47:28.276Z",
                    "email": "user@example.com",
                    "phone": "string"
                }
            },
        ),
    ],
    url_path='register',
    detail=False,
    url_name='register',
)


token_refresh_decorator = custom_decorator(
    request=TokenRefreshSerializer,
    responses=TokenRefreshSerializer,
    summary='refresh expired access token',
    methods=['POST'],
    url_path='token/refresh',
    detail=False,
    url_name='refresh_token',
)


users_list_decorator = extend_schema(
    responses=UserSerializer(many=True),
    summary='List of users',
    methods=['GET'],
)

user_retrieve_decorator = extend_schema(
    responses=UserSerializer,
    summary='Get a specific user by ID',
    methods=['GET'],
)

user_update_decorator = extend_schema(
    request=UserSerializer(partial=True),
    responses={200: 'application/json'},
    methods=['PUT'],
    summary='Update a user',
    description='Update a specific user by its ID, only the user itself or admin can perform this action',
    examples=[
        OpenApiExample(
            name='Successful update response',
            response_only=True,
            status_codes=["200"],
            value={'response': 'Updated successfully'}
        )
    ]
)

user_delete_decorator = extend_schema(
    responses={204: 'application/json'},
    methods=['DELETE'],
    summary='Delete a user',
    description='Delete a specific user by its ID, only the user itself or admin can perform this action',
    examples=[
        OpenApiExample(
            name='Successful deleted response',
            response_only=True,
            status_codes=["204"],
            value={'response': 'Deleted successfully'}
        )
    ]
)
