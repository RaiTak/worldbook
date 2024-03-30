from django.db import models
from django.urls import reverse
from PIL import Image as PilImage


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL-адрес')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True, verbose_name='Иконка')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:book_list', kwargs={'slug': self.slug, 'type': 'category'})


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL-адрес')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    icon = models.ImageField(upload_to='genre_icons/', blank=True, null=True, verbose_name='Иконка')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:book_list', kwargs={'slug': self.slug, 'type': 'genre'})


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL-адрес')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    icon = models.ImageField(upload_to='tag_icons/', blank=True, null=True, verbose_name='Иконка')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:book_list', kwargs={'slug': self.slug, 'type': 'tag'})


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя', help_text='Введите имя автора')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', help_text='Введите фамилию автора')
    photo = models.ImageField(upload_to='author_photos/', blank=True, null=True, verbose_name='Фотография')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL-адрес')
    biography = models.TextField(verbose_name='Биография', help_text='Краткая биография автора', blank=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('catalog:book_list', kwargs={'slug': self.slug, 'type': 'author'})

    def get_type(self):
        return "Author"


class Book(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', help_text="Введите название книги")
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL-адрес')
    image = models.ImageField(upload_to='cover_images/', blank=True, null=True, verbose_name='Обложка')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    year = models.PositiveIntegerField(verbose_name='Год издания')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='books', verbose_name='Категория')
    genre = models.ManyToManyField(Genre, blank=True, related_name='books', verbose_name='Жанр')
    authors = models.ManyToManyField(Author, blank=True, related_name='books', verbose_name='Автор(ы)')
    tags = models.ManyToManyField(Tag, blank=True, related_name='books', verbose_name='Тэг')
    isbn = models.CharField(max_length=50, blank=True, null=True, verbose_name='ISBN')
    pages = models.PositiveIntegerField(null=True, blank=True, verbose_name='Количество страниц')
    language = models.CharField(max_length=100, blank=True, verbose_name='Язык')
    publisher = models.CharField(max_length=200, blank=True, null=True, verbose_name='Издательство')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    format = models.CharField(max_length=100, blank=True, null=True, verbose_name='Формат')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')

    class Meta:
        ordering = ['name']
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