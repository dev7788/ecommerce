from django.db import models
from django.urls import reverse

from registration.models import User


class ProductCategory(models.Model):
    """
    Specific category for each product
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Describes each product
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    price = models.FloatField(default=0.0)
    discount_percent = models.FloatField(default=0.0)
    rating = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.pk)])

    @property
    def discount_price(self):
        return self.price - int((self.price * (self.discount_percent / 100)))

    @property
    def stars(self):
        print(self.rating, 5-self.rating)
        return range(self.rating)

    @property
    def stars_empty(self):
        return range(5 - self.rating)

    @property
    def featured_image(self):
        image = self.image_set.filter(featured_image=True)
        if image.count() > 0:
            return image[0].image_path
        return None

    def __str__(self):
        return self.name


class Image(models.Model):
    """
    Image associated with a product
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image_path = models.ImageField(upload_to='products/')
    featured_image = models.BooleanField(default=False)

    def __str__(self):
        return "{0} - {1}".format(self.product.name, self.name)


class Cart(models.Model):
    """
    Shopping cart for users to add products
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "{0} - {1}".format(self.user.username, self.product.name)
