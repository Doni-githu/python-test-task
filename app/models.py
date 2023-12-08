from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Comic(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.title


class Rating(models.Model):
    comic_id = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name="comic")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return str(self.value)
