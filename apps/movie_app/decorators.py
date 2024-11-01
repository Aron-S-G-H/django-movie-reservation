from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiTypes
from . import serializer
from utils.custom_decorator import custom_decorator


genre_list_decorator = extend_schema(
    responses=serializer.MovieGenreSerializer(many=True),
    methods=['GET'],
    summary='List of movies genre',
)

genre_retrieve_decorator = extend_schema(
    responses=serializer.MovieGenreSerializer,
    methods=['GET'],
    summary='Get a specific genre with ID',
)

genre_create_decorator = extend_schema(
    request=serializer.MovieGenreSerializer,
    responses={201: 'application/json'},
    methods=['POST'],
    summary='Create a movie genre',
    description='Create a movie genre, only admin can perform this action',
    examples=[
        OpenApiExample(
            name='Successful create response',
            response_only=True,
            status_codes=["201"],
            value={'response': 'Created successfully'}
        )
    ]
)

genre_update_decorator = extend_schema(
    request=serializer.MovieGenreSerializer(partial=True),
    responses={200: 'application/json'},
    methods=['PUT'],
    summary='Update a genre',
    description='Update a specific genre by its ID, only admin can perform this action',
    examples=[
        OpenApiExample(
            name='Successful update response',
            response_only=True,
            status_codes=["200"],
            value={'response': 'Updated successfully'}
        )
    ]
)

genre_delete_decorator = extend_schema(
    responses={204: 'application/json'},
    methods=['DELETE'],
    summary='Delete a genre',
    description='Delete a specific genre by its ID, only admin can perform this action',
    examples=[
        OpenApiExample(
            name='Successful deleted response',
            response_only=True,
            status_codes=["204"],
            value={'response': 'Deleted successfully'}
        )
    ]
)

movie_list_decorator = extend_schema(
    responses=serializer.MovieSerializer(many=True),
    methods=['GET'],
    summary='Movies list',
)

movie_retrieve_decorator = extend_schema(
    responses=serializer.MovieSerializer,
    methods=['GET'],
    summary='Get a specific movie with ID'
)

movie_create_decorator = extend_schema(
    request=serializer.MovieSerializer,
    responses={201: 'application/json'},
    methods=['POST'],
    summary='Create a new movie',
    description='Create a movie, only admin can perform this action',
    examples=[
        OpenApiExample(
            name='Successful create response',
            response_only=True,
            status_codes=["201"],
            value={'response': 'Created successfully'}
        )
    ]
)

movie_update_decorator = extend_schema(
    request=serializer.MovieSerializer(partial=True),
    responses={200: 'application/json'},
    methods=['PUT'],
    summary='Update a movie',
    description='Update a specific movie by its ID, only admin can perform this action',
    examples=[
        OpenApiExample(
            name='Successful update response',
            response_only=True,
            status_codes=["200"],
            value={'response': 'Updated successfully'}
        )
    ]
)

movie_delete_decorator = extend_schema(
    responses={204: 'application/json'},
    methods=['DELETE'],
    summary='Delete a movie',
    description='Delete a specific movie by its ID, only admin can perform this action',
    examples=[
        OpenApiExample(
            name='Successful deleted response',
            response_only=True,
            status_codes=["204"],
            value={'response': 'Deleted successfully'}
        )
    ]
)

movie_showtime_decorator = custom_decorator(
    parameters=[
        OpenApiParameter(
            name='date',
            type=OpenApiTypes.DATE,
            required=True,
            location=OpenApiParameter.QUERY,
            description="Date to filter movies with showtimes",
        )
    ],
    summary='Movies show time for specific date',
    description='Get a list of movies show time for a specific date along with movie info',
    responses=serializer.MovieSerializer(many=True),
    methods=['GET'],
    url_path='showtime',
    url_name='showtime',
    detail=False,
)

available_seats_decorator = custom_decorator(
    detail=True,
    methods=['GET'],
    url_path='available_seats',
    url_name='available_seat',
    responses=serializer.SeatSerializer(many=True),
    summary='Available seats for a show time',
    description='Get a list of available seats for a show time by show time ID'
)

reservation_list_decoration = extend_schema(
    responses=serializer.ReservationSerializer(many=True),
    methods=['GET'],
    summary='Reservations list',
)

reservation_create_decorator = extend_schema(
    request=serializer.ReservationCreateSerializer,
    responses={201: 'application/json'},
    summary='Create a reservation with selected showtime and seats',
    description='Endpoint to create a reservation for a specific showtime and selected seats',
    examples=[
        OpenApiExample(
            name='Successful create response',
            response_only=True,
            status_codes=["201"],
            value={'response': 'Created successfully'}
        )
    ]
)

reservation_cancel_decorator = custom_decorator(
    parameters=[
        OpenApiParameter(
          name='reservation ID',
          required=True,
          type=OpenApiTypes.INT,
          location=OpenApiParameter.PATH,
        ),
    ],
    responses={204: 'application/json'},
    examples=[
        OpenApiExample(
            name='Successful deleted response',
            response_only=True,
            status_codes=["204"],
            value={'response': 'Deleted successfully'}
        )
    ],
    summary='Delete & cancel a reservation by ID',
    methods=['DELETE'],
    url_path='cancel',
    url_name='cancel_reservation',
    detail=False,
)
