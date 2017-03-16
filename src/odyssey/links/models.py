from django.db import models


class MyLink(models.Model):
    slug = models.SlugField(
        max_length=255,
        default=''
    )
    name = models.CharField(
        max_length=255,
        default=''
    )
    link = models.CharField(
        max_length=255,
        default=''
    )
    order = models.SmallIntegerField(
        default=0
    )
    blank = models.BooleanField(
        default=True
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if MyLink.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['order', 'name']
