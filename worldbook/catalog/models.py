from django.db import models
from django.urls import reverse
from PIL import Image as PilImage


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:catalog', kwargs={'category_slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='cover_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='books')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('catalog:book', kwargs={'book_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = PilImage.open(img_path)

            # Уменьшаем изображение, сохраняя пропорции
            img.thumbnail((300, 300), PilImage.Resampling.LANCZOS)

            # Если вы хотите обрезать изображение до точного размера 300x300 после уменьшения
            width, height = img.size  # Получаем размеры после уменьшения
            if width != 300 or height != 300:
                # Находим центральную точку
                left = (width - 300) / 2
                top = (height - 300) / 2
                right = (width + 300) / 2
                bottom = (height + 300) / 2

                # Обрезаем изображение до центральных 300x300
                img = img.crop((left, top, right, bottom))

            # Сохраняем изменения
            img.save(img_path)