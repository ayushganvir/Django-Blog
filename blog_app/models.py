from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify


def slug_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.slug, filename)

posts= Post.Objects.filter(title__startswith = '')
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(default=slugify(title), max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=slug_directory_path, default='default.jpg')

    class Status(models.TextChoices):
        DRAFT = 'D', _("Draft")
        PUBLISH = 'P', _("Publish")

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    comment_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments', null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.comment_maker.username)