from django.db import models


class Customer(models.Model):

    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('manager', 'Hotel Manager'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=50, unique=True)

    password = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    mobile = models.CharField(max_length=15)

    address = models.CharField(max_length=300)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )

    def __str__(self):
        return self.username


class Restaurant(models.Model):

    owner = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="owned_restaurants",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    picture = models.URLField(
        default='https://designshack.net/wp-content/uploads/Free-Simple-Restaurant-Logo-Template.jpg'
    )

    cuisine = models.CharField(max_length=200)

    rating = models.FloatField(default=4.0)

    approved = models.BooleanField(default=False)

    location = models.CharField(max_length=300, default="Gadag")

    def __str__(self):
        return self.name


class Item(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="items"
    )

    name = models.CharField(max_length=100)

    description = models.TextField()

    price = models.FloatField()

    vegeterian = models.BooleanField(default=False)

    picture = models.URLField(
        default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg'
    )

    def __str__(self):
        return self.name


class Cart(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    items = models.ManyToManyField(Item)

    def total_price(self):
        return sum(item.price for item in self.items.all())


class Order(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    items = models.ManyToManyField(Item)

    total_amount = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=50,
        default="Preparing"
    )

    def __str__(self):
        return f"{self.customer.username} - {self.restaurant.name}"