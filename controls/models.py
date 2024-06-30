from django.shortcuts import render
from django.db import models
from authentication.models import CustomUser


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    product_size = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    main_image_url = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/products', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.product_name}"

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    product_discription = models.TextField()
    image = models.ImageField(upload_to='newsletter_images/')
    posted_date = models.DateField(auto_now_add=True)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    posted_date = models.DateField(auto_now_add=True)

    def update_post(self, title, description, image):
        self.title = title
        self.description = description
        if image:
            self.image = image
        self.save()

    def delete_post(self):
        self.delete()

class Order(models.Model):
    order_date = models.DateField()
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', default=1)
    products = models.ManyToManyField(Product)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer.full_name} - Order ID: {self.id}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"