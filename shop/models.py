from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Variation(models.Model):
    name = models.CharField(max_length=10, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name

class Rating(models.Model):
    name = models.ForeignKey(User,
                              related_name='ratings',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    detail = models.CharField(max_length=500, blank=True)
    rate = models.IntegerField()
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', args=[self.id])


    
class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=300, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    brands = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    variation = models.ManyToManyField(Variation, blank=True)
    detail = models.TextField(max_length=1000, null=True, blank=True)
    specification = models.CharField(max_length=1000, null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    second_image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    third_image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('created',) 
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name
    #pylint: disable=E1101
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


