
from django.utils.text import slugify
from unidecode import unidecode

def unique_slugify(instance, value, slug_field_name='slug'):
    value = unidecode(value)
    slug = slugify(value)
    ModelClass = instance.__class__
    unique_slug = slug
    num = 1

    while ModelClass.objects.filter(**{slug_field_name:unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{num}"

    return unique_slug