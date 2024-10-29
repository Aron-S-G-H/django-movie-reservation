from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MovieGenre(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    is_active = models.BooleanField(db_default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(MovieGenre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Movie(BaseModel):
    genre = models.ForeignKey(MovieGenre, on_delete=models.SET_NULL, null=True, related_name='movies')
    title = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    director = models.CharField(max_length=128, blank=True, null=True)
    duration = models.PositiveSmallIntegerField(help_text="Duration in minutes", null=True, blank=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=128, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class MoviePoster(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='posters')
    poster = models.ImageField(upload_to='posters', width_field='poster_width', height_field='poster_height')
    poster_width = models.PositiveSmallIntegerField(null=True, blank=True)
    poster_height = models.PositiveSmallIntegerField(null=True, blank=True)
    size = models.FloatField(blank=True, help_text='in kilobytes')

    def save(self, *args, **kwargs):
        self.size = self.poster.size / 1000
        super(MoviePoster, self).save(*args, **kwargs)

    def __str__(self):
        return self.movie.title


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    start_time = models.TimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.start_time} on {self.show_date}"


class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.PositiveSmallIntegerField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} for {self.showtime}"

