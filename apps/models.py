from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, CharField, TextChoices, Model, DateField, SlugField, FloatField, \
    PositiveSmallIntegerField, ForeignKey, TextField, CASCADE, DateTimeField, EmailField, IntegerField
from django.db.models.functions import Now
from django.forms import IntegerField
from django.utils.text import slugify


# Create your models here.

class CreateBaseModel(Model):
    class Meta:
        abstract = True

    created_at = DateTimeField(auto_now_add=True, db_default=Now())
    updated_at = DateTimeField(auto_now=True, db_default=Now())


class SlugBaseModel(Model):
    class Meta:
        abstract = True

    slug = SlugField(max_length=255, unique=True, editable=False)
    name = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True, db_default=Now())
    updated_at = DateTimeField(auto_now=True, db_default=Now())

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.first(slug=self.slug).exist():
            self.slug += '-1'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Emialfield must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
class User(AbstractUser):
    class StatusType(TextChoices):
        ADMIN = 'Admin', 'admin'
        CUSTOMER = 'Customer', 'cuestomer'

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    yoshi=IntegerField(max_value=150)
    image = ImageField(upload_to='users/%Y/%m/%d')
    email = EmailField(unique=True, blank=True,max_length=254)
    phone_number = CharField(max_length=25, null=True, blank=True)
    mobile_number = CharField(max_length=25, null=True, blank=True)
    status_type = CharField(max_length=15, choices=StatusType.choices, default=StatusType.CUSTOMER)


class Category(SlugBaseModel):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(SlugBaseModel):
    price = FloatField(help_text="Price in UZB so'm")
    quantity = IntegerField()
    discount = PositiveSmallIntegerField(default=0, help_text='Discount in Percentage(%)')
    category = ForeignKey('apps.Category', CASCADE)
    shipping_cost = FloatField(help_text='Cost of Delivery')
    description = TextField(null=True, blank=True)


class Image(CreateBaseModel):
    image = ImageField(upload_to='products/%Y/%m/%d/')
    product = ForeignKey('apps.Product', CASCADE)

    def delete(self, using=None, keep_parents=False):
        self.image.delete(False)
        return super().delete(using, keep_parents)
