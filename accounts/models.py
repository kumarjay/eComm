from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
import uuid
from base.models import BaseModel
from products.models import Product
from django.utils.text import slugify

# class CustomerUser(AbstractBaseUser):
#     address = models.CharField()


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False,
                                        cart__user= self.user).count()
    
    # def save(self, *args, **kwargs):
    #     self.uuid = uuid(self.user)
    #     super(Profile, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.user)


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='carts')
    is_paid = models.BooleanField(default=False)
    def __str__(self) -> str:
        return str(self.user)


class CartItems(BaseModel):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             related_name='cart_items')
    products = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    items = models.IntegerField(null=True)
    total_price = models.FloatField(null=True)
    def __str__(self) -> str:
        return str(self.cart.user) + ' --> ' + str(self.products.product_name)



