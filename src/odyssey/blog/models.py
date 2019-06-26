from django.db import models


class Category(models.Model):
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    order = models.IntegerField(
        default=10
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<Category %s>' % self.name

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Category.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
