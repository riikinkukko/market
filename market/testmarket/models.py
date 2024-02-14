from django.db import models
from django.urls import reverse

class Good(models.Model):
    name = models.CharField(max_length=55)
    price = models.IntegerField()
    is_avail = models.BooleanField()
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})

class Basket(models.Model):
    user_id = models.IntegerField()
    goods_id = models.TextField()