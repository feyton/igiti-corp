from datetime import datetime

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# from user.models import User
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from hitcount.models import HitCount, HitCountMixin

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forestry:category', kwargs={'pk': self.id})


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facebook = models.CharField(
        _('author facebook'), max_length=255, blank=True)
    twitter = models.CharField(_('author twitter'), max_length=255, blank=True)
    telephone = models.CharField(_('telephone'), max_length=13, blank=True)
    image = models.ImageField(
        _('Author Image'), upload_to='author', blank=True, null=True)
    bio = models.TextField(_('author biography'), blank=True)

    def __str__(self):
        full_name = self.user.get_full_name()
        return str(full_name)

    def get_author_name(self):
        return self.user.first_name

    def get_absolute_url(self):
        return reverse('author:detail', kwargs={'user': self.user.id})


class BlogPostQueryset(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def draft(self):
        return self.filter(published=False)


class BlogPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    image = models.ImageField(_('image'), blank=True,
                              null=True, upload_to='blog')
    text = RichTextUploadingField(_('text'))
    description = models.TextField(_('description'), blank=True, null=True)
    published = models.BooleanField(_('published'), default=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    pub_date = models.DateTimeField(_('publish date'), blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    objects = BlogPostQueryset.as_manager()

    class Meta:
        # This class help to specify the plural and structure in admin section
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['-pub_date']

    def save(self, *args, **kwargs):
        if self.published and self.pub_date is None:
            self.pub_date = datetime.now()
        elif not self.published and self.pub_date is not None:
            self.pub_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forestry:detail', kwargs={'slug': self.slug})

    def get_author(self):
        if author:
            return self.author.get_author_name()

    def get_bio(self):
        return self.author.bio[:200]

    def get_author_image(self):
        return self.author.image.url
