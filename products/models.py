from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from accounts.models import CustomUser


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    sub_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='sub_categorys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class ProductMedia(models.Model):
    name = models.CharField(max_length=100)
    TYPE_MEDIA = (('img', 'عکس ها'), ('video', 'فیلم'))
    type = models.CharField(choices=TYPE_MEDIA, max_length=5)
    image = models.ImageField(upload_to='media-products/img/', null=True, blank=True)
    video = models.FileField(upload_to='media-products/video/', null=True, blank=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug + ' - ' + self.type

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.ManyToManyField(ProductCategory, related_name='products')
    media = models.ManyToManyField(ProductMedia, related_name='products')
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    count_inventory = models.PositiveIntegerField(default=0)
    is_home_index = models.BooleanField(default=False) #توی صفحه اصلی نمایش داده بشه یا نه
    is_active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        if self.discount > 0:
            return self.price - self.discount
        else:
            return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_down = models.BooleanField(
        default=False)  # زمانی که خرید تکمیل میشود این ترو میشه و مقادیر زیر مقدار میگیرند برای ثبت شدن در هیستوری
    price = models.PositiveIntegerField(null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                condition=Q(is_down=False),
                name='unique_open_cart_item'
            )
        ]

    def __str__(self):
        return self.user.username

    @property
    def unit_price(self):
        if self.is_down and self.price is not None:
            discount = self.discount or 0
            return max(self.price - discount, 0)
        return self.product.final_price

    @property
    def line_total(self):
        return self.unit_price * self.quantity
