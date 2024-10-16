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
