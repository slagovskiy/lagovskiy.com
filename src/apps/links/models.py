from django.db import models


class MyLinks(models.Model):
    name = models.CharField(
        max_length=255,
        default=''
    )
    link = models.URLField(
        default=''
    )
    order = models.SmallIntegerField(
        default=0
    )
    new_window = models.BooleanField(
        default=True
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']
