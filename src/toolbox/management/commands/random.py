from random import randint
from apps.blog.models import Tag, Category
from faker import Factory
from django.core.management.base import BaseCommand

fake_ru = Factory.create('ru-RU')
fake_en = Factory.create('en-US')
fake = None


def clean():
    Tag.objects.all().delete()
    Category.objects.all().delete()

def blog_tag(count):
    for _ in range(0, count):
        if randint(0, 1):
            fake = fake_ru
        else:
            fake = fake_en
        slug = fake.slug()
        name = fake.word()
        if not Tag.exist(slug):
            t = Tag.objects.create(
                slug=slug,
                name=name
            )
            t.save()
            print(t)


def blog_category(count):
    for _ in range(0, count):
        if randint(0, 1):
            fake = fake_ru
        else:
            fake = fake_en
        slug = fake.slug()
        name = fake.word()
        if not Category.exist(slug):
            c = Category.objects.create(
                slug=slug,
                name=name
            )
            c.save()
            print(c)


class Command(BaseCommand):
    help = 'generate random data'

    def handle(self, **options):
        clean()
        blog_category(10)
        blog_tag(50)
