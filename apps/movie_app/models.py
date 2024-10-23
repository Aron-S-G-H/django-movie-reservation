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
