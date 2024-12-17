import random
from django.core.management.base import BaseCommand
from faker import Faker
from apps.account_app.models import CustomUser
from apps.movie_app.models import MovieGenre, Movie, MoviePoster, Seat, Showtime, Reservation


class Command(BaseCommand):
    help = 'Generate fake data for models'

    def handle(self, *args, **options):
        fake = Faker()
        self._generate_users(fake, count=5)
        self._generate_movie_genres(fake, count=5)
        self._generate_movies(fake, count=5)
        self._generate_movie_posters(fake, count=5)
        self._generate_showtimes(fake, count=5)
        self._generate_seats(fake, count=30)
        self._generate_reservation(fake, count=10)
        self.stdout.write(self.style.SUCCESS('Fake data generation completed!'))

    def _generate_users(self, fake, count):
        users = []
        for _ in range(count):
            phone_number = f'09{random.randint(100000000, 999999999)}'
            email = fake.unique.email()
            user = CustomUser(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=phone_number,
                email=email,
                is_active=True,
            )
            user.set_password('password123')
            users.append(user)
        CustomUser.objects.bulk_create(users)
        self.stdout.write(f'{count} CustomUser records created.')

    def _generate_movie_genres(self, fake, count):
        genres = []
        for _ in range(count):
            name = fake.unique.word().capitalize(),
            genre = MovieGenre(
                name=name,
                description=fake.text(max_nb_chars=200),
                slug=name,
            )
            genres.append(genre)
        MovieGenre.objects.bulk_create(genres)
        self.stdout.write(f'{count} MovieGenre records created.')

    def _generate_movies(self, fake, count):
        genres = list(MovieGenre.objects.all())
        movies = []
        for _ in range(count):
            genre = random.choice(genres) if genres else None
            title = fake.unique.sentence(nb_words=3)
            movie = Movie(
                genre=genre,
                title=title,
                description=fake.text(),
                release_date=fake.date_between(start_date='-5y', end_date='today'),
                director=fake.name(),
                duration=random.randint(80, 180),
                language=fake.language_name(),
                slug=title,
            )
            movies.append(movie)
        Movie.objects.bulk_create(movies)
        self.stdout.write(f'{count} MovieGenre records created.')

    def _generate_movie_posters(self, fake, count):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile

        movies = list(Movie.objects.all())
        for _ in range(count):
            movie = random.choice(movies)
            # Create a placeholder image
            img = Image.new('RGB', (500, 700), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            img_buffer = BytesIO()
            img.save(img_buffer, format='JPEG')
            img_buffer.seek(0)
            poster = MoviePoster(
                movie=movie,
            )
            poster.poster.save(f'{fake.unique.word()}.jpg', ContentFile(img_buffer.read()), save=True)
        self.stdout.write(f'{count} MoviePoster records created.')

    def _generate_showtimes(self, fake, count):
        movies = list(Movie.objects.all())
        showtimes = []
        for _ in range(count):
            movie = random.choice(movies)
            show_date = fake.date_between(start_date='-30d', end_date='+30d')
            start_time = fake.time_object()
            showtime = Showtime(
                movie=movie,
                show_date=show_date,
                start_time=start_time,
            )
            showtimes.append(showtime)
        Showtime.objects.bulk_create(showtimes)
        self.stdout.write(f'{count} Showtime records created.')

    def _generate_seats(self, fake, count):
        showtimes = list(Showtime.objects.all())
        seats = []
        for _ in range(count):
            showtime = random.choice(showtimes)
            seat = Seat(
                showtime=showtime,
                seat_number=random.randint(10, 100),
                is_reserved=random.choice([True, False]),
            )
            seats.append(seat)
        Seat.objects.bulk_create(seats)
        self.stdout.write(f'{count} Seat records created.')

    def _generate_reservation(self, fake, count):
        users = list(CustomUser.objects.all())
        showtimes = list(Showtime.objects.all())
        for _ in range(count):
            user = random.choice(users)
            showtime = random.choice(showtimes)
            movie = showtime.movie
            available_seats = Seat.objects.filter(showtime=showtime, is_reserved=False)
            if not available_seats:
                self.stdout.write(self.style.WARNING(f"No available seats for showtime {showtime.id}."))
                continue
            if Reservation.objects.filter(user=user, movie=movie, showtime=showtime).exists():
                continue
            # Reserve 1-5 random seats
            max_seats_to_reserve = min(len(available_seats), random.randint(1, 5))
            if max_seats_to_reserve == 0:
                continue
            reserved_seats = random.sample(list(available_seats), k=max_seats_to_reserve)
            reservation = Reservation.objects.create(
                user=user,
                movie=movie,
                showtime=showtime,
            )
            reservation.seats.set(reserved_seats)
            # Mark seats as reserved
            available_seats.filter(id__in=[seat.id for seat in reserved_seats]).update(is_reserved=True)
        self.stdout.write(self.style.SUCCESS(f'{count} Reservations created successfully!'))
