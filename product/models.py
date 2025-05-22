from datetime import date
from django.db import models
from django.urls import reverse
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.hashers import make_password, check_password


# <================> ABSTRACT MODELS <================> #
# <========> SOCIAL MEDIA MODEL <========> #
class SocialMedia(models.Model):
    facebook = models.URLField(
        blank=True,
        null=True,
        verbose_name="Facebook linki",
    )
    instagram = models.URLField(
        blank=True,
        null=True,
        verbose_name="Instagram linki",
    )
    linkedin = models.URLField(
        blank=True,
        null=True,
        verbose_name="LinkedIn linki",
    )
    youtube = models.URLField(
        blank=True,
        null=True,
        verbose_name="YouTube linki",
    )

    class Meta:
        abstract = True


# <================> TAG MODEL <================> #
class Tag(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name="Ad",
    )
    status = models.BooleanField(
        default=True,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaranma tarixi",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yenilənmə tarixi",
    )

    def get_absolute_url(self):
        return reverse("product:tag_products", kwargs={"tag_id": self.id})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ("-created_at",)


# <================> CATEGORY MODEL <================> #
class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Ad",
    )
    icon = models.FileField(
        upload_to="category/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["svg", "png", "jpg", "jpeg"]
            )
        ],
        verbose_name="Şəkil",
    )
    status = models.BooleanField(
        default=True,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaranma tarixi",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yenilənmə tarixi",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "product:category_products", kwargs={"category_id": self.id}
        )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("-created_at",)


# <================> GENDER MODEL <================> #
class Gender(models.Model):
    name = models.CharField(max_length=300, verbose_name="Ad")
    status = models.BooleanField(
        default=True,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaranma tarixi",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yenilənmə tarixi",
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Genders"
        ordering = ("-created_at",)


# <================> AUTHOR MODEL <================> #
class Author(SocialMedia, models.Model):
    username = models.CharField(max_length=100, verbose_name="İstiadəçi adı", null=True)
    password = models.CharField(max_length=100, verbose_name="Şifrə", null=True)
    email = models.EmailField(max_length=254, verbose_name="E-poçt", null=True)
    
    name = models.CharField(max_length=300, verbose_name="Ad",)
    surname = models.CharField(max_length=300, verbose_name="Soyad",)
    image = models.FileField(
        upload_to="author/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["svg", "png", "jpg", "jpeg"]
            )
        ],
        null=True,
        blank=True,
        verbose_name="Şəkil",
    )
    gender = models.ForeignKey(
        Gender,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Cinsi",
    )
    bio = RichTextUploadingField(
        blank=True,
        null=True,
        verbose_name="Bioqrafiya",
    )
    birthday = models.DateField(
        verbose_name="Doğum tarixi",
    )
    status = models.BooleanField(
        default=True,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaranma tarixi",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yenilənmə tarixi",
    )

    def __str__(self):
        return f"{self.name} {self.surname}"

    def get_age(self):
        today = date.today()
        age = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def a_check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ("-created_at",)


# <================> PRODUCT MODEL <================> #
class Product(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name="Ad",
    )
    description = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name="Ətraflı",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Qiymət",
    )
    tax_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Tax qiymət",
    )
    discount = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        verbose_name="Endirim (%)",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        verbose_name="Categoriya",
    )
    poster = models.FileField(
        upload_to="product/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["svg", "png", "jpg", "jpeg"]
            )
        ],
        verbose_name="Şəkil",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Tags",
    )
    coupon = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Kupon",
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Müəllif",
    )
    status = models.BooleanField(
        default=True,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaranma tarixi",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yenilənmə tarixi",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"product_id": self.pk})
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-created_at",)

# <================> PRODUCT IMAGE MODEL <================> #
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Məhsul",
    )
    image = models.ImageField(
        upload_to="product/gallery/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["svg", "png", "jpg", "jpeg"]
            )
        ],
        verbose_name="Şəkil",
    )

    def __str__(self):
        return f"{self.product.name} Image"
    
    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


# <================> PROXY MODELS <================> #
# <========> SALE PRODUCT MODEL <========> #
class SaleProduct(Product):
    class Meta:
        verbose_name = "Sale Product"
        verbose_name_plural = "Sale Products"
        proxy = True


# <========> NEW COLLECTION MODEL <========> #
class NewCollection(Product):
    class Meta:
        verbose_name = "New Collection"
        verbose_name_plural = "New Collections"
        proxy = True
