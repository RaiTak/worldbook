from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.db import models

user_model = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликован'

    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name='URL-адресс')
    content = models.TextField(verbose_name='Статья')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    author = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={
            'year': self.publish.year,
            'month': self.publish.month,
            'day': self.publish.day,
            'slug': self.slug
        })

