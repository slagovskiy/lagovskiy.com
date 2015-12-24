from django.db import models


class MyLinks(models.Model):
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']
