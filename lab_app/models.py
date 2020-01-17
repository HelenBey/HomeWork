from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):
    class Meta:
        db_table = 'films'

    name = models.CharField(max_length=255)

    description = models.CharField(max_length=1000)

    image = models.ImageField(upload_to='lab_app/static/film_images',
                              default='lab_app/static/film_images/default.png')

    def image_path(self):
        return self.image.name.replace('lab_app/', '')

    def short_description(self):
        return self.description[:126]

    def __str__(self):
        return ' '.join([
            self.name,
            ' from ',
            self.seller,
        ])


class Review(models.Model):
    class Meta:
        db_table = 'reviews'

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    description = models.CharField(
        max_length=500,
    )

    def __str__(self):
        return ' '.join([
            'review \'',
            str(self.description),
            ' \' from user @',
            str(self.user.username),
        ])
