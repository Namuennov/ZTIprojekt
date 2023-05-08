from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model


class Nationality(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    activityPeriod = models.CharField(max_length=30)
    description = models.CharField(max_length=1200)
    nationalityId = models.ForeignKey(Nationality, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='authorsImages/', blank=True, default='authorsImages/default.jpg')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Opus(models.Model):
    name = models.CharField(max_length=100)
    categoryId = models.ForeignKey(Category, on_delete=models.RESTRICT)
    authorId = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=1200)
    image = models.ImageField(upload_to='opusesImages/', blank=True, default='opusesImages/default.jpg')

    def __str__(self):
        return self.name

class Review(models.Model):
    content = models.CharField(max_length=15000)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    userId = models.ForeignKey(get_user_model(), default=-1, on_delete=models.SET_DEFAULT)
    opusId = models.ForeignKey(Opus, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:50]

class Comment(models.Model):
    content = models.CharField(max_length=1500)
    userId = models.ForeignKey(get_user_model(), default=-1, on_delete=models.SET_DEFAULT)
    reviewId = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:50]

class OpusList(models.Model):
    name = models.CharField(max_length=100)
    userId = models.ForeignKey(get_user_model(), default=-1, on_delete=models.SET_DEFAULT)
    opuses = models.ManyToManyField(Opus)

    def __str__(self):
        return self.name

#to ewentualnie mozna wyrzucic
class UserRating(models.Model):
    userId = models.ForeignKey(get_user_model(), default=-1, on_delete=models.SET_DEFAULT)
    opusId = models.ForeignKey(Opus, on_delete=models.CASCADE)
    hoursToFinish = models.IntegerField(default=0)
    difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
