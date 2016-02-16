from random import randint
from apps.blog.models import Tag, Category
from apps.links.models import MyLink
from faker import Factory
from django.core.management.base import BaseCommand

fake_ru = Factory.create('ru-RU')
fake_en = Factory.create('en-US')
fake = None


def clean():
    MyLink.objects.all().delete()
    Tag.objects.all().delete()
    Category.objects.all().delete()


def links_mylink():
    slug = 'facebook'
    name = '<i class="fa fa-facebook-official"></i> i on facebook'
    link = 'https://www.facebook.com/sergey.lagovskiy'
    ml = MyLink.objects.create(
        slug=slug,
        name=name,
        link=link,
        order=10
    )
    ml.save()
    slug = 'flickr'
    name = '<i class="fa fa-flickr"></i>  my photos on flickr'
    link = 'https://www.flickr.com/photos/slagovskiy/'
    ml = MyLink.objects.create(
        slug=slug,
        name=name,
        link=link,
        order=20
    )
    ml.save()
    slug = 'github'
    name = '<i class="fa fa-github-square"></i> my code on github'
    link = 'https://github.com/slagovskiy'
    ml = MyLink.objects.create(
        slug=slug,
        name=name,
        link=link,
        order=30
    )
    ml.save()
    slug = 'email'
    name = '<i class="fa fa-envelope-square"></i> write me email'
    link = 'mailto:slagovskiy@gmail.com'
    blank = False
    ml = MyLink.objects.create(
        slug=slug,
        name=name,
        link=link,
        order=40,
        blank=blank
    )
    ml.save()
    slug = 'hh'
    name = '<i class="fa fa-user"></i> headhunt me'
    link = 'http://novosibirsk.hh.ru/resume/4f27274aff01958a560039ed1f7a44564d3256'
    ml = MyLink.objects.create(
        slug=slug,
        name=name,
        link=link,
        order=50
    )
    ml.save()


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
    # for _ in range(0, count):
    #     if randint(0, 1):
    #         fake = fake_ru
    #     else:
    #         fake = fake_en
    #     slug = fake.slug()
    #     name = fake.word()
    #     if not Category.exist(slug):
    #         c = Category.objects.create(
    #             slug=slug,
    #             name=name,
    #             order=randint(1, 100)
    #         )
    #         c.save()
    #         print(c)
    slug = 'admin'
    name = 'Админево'
    c = Category.objects.create(
        slug=slug,
        name=name,
        order=10
    )
    c.save()
    slug = 'dev'
    name = 'Разработка'
    c = Category.objects.create(
        slug=slug,
        name=name,
        order=20
    )
    c.save()
    slug = 'photo'
    name = 'Фотография'
    c = Category.objects.create(
        slug=slug,
        name=name,
        order=30
    )
    c.save()
    slug = 'other'
    name = 'Разное'
    c = Category.objects.create(
        slug=slug,
        name=name,
        order=40
    )
    c.save()


class Command(BaseCommand):
    help = 'generate random data'

    def handle(self, **options):
        clean()
        blog_category(5)
        blog_tag(50)
        links_mylink()
