from datetime import datetime
from random import randint, choice
from apps.blog.models import Tag, Category, Post, Comment
from apps.links.models import MyLink
from apps.userext.models import User
from faker import Factory
from django.core.management.base import BaseCommand
from django.utils import timezone

fake_ru = Factory.create('ru-RU')
fake_en = Factory.create('en-US')
fake = None


def clean():
    MyLink.objects.all().delete()
    Post.objects.all().delete()
    Comment.objects.all().delete()
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
    print(ml)
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
    print(ml)
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
    print(ml)
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
    print(ml)
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
    print(ml)


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
    print(c)
    slug = 'dev'
    name = 'Разработка'
    c = Category.objects.create(
        slug=slug,
        name=name,
        order=20
    )
    c.save()
    print(c)
    slug = 'photo'
    name = 'Фотография'
    c = Category.objects.create(
        slug=slug,
        name=name,
        order=30
    )
    c.save()
    print(c)
    slug = 'other'
    name = 'Разное'
    c = Category.objects.create(
        slug=slug,
        name=name,
        order=40
    )
    c.save()
    print(c)


def blog_post(count):
    for _ in range(0, count):
        if randint(0, 1):
            fake = fake_ru
        else:
            fake = fake_en
        slug = fake.slug()
        title = ' '.join(fake.words(randint(1, 6)))
        title = title[0:1].upper() + title[1:]
        author = User.objects.all().first()
        description = ' '.join(fake.words(randint(5, 20)))
        keywords = ', '.join(fake.words(randint(5, 20)))
        status = randint(0, 2)
        sticked = False
        if randint(0, 1):
            sticked = True
        comments_enabled = False
        if randint(0, 1):
            comments_enabled = True
        comments_moderated = False
        if randint(0, 1):
            comments_moderated = True
        do_ping = False
        if randint(0, 1):
            do_ping = True
        published = None
        if status == 2:
            published = timezone.now()
        categories = []
        for __ in range(1, randint(2, 4)):
            categories.append(choice(Category.objects.all()))
        tags = []
        for __ in range(1, randint(1, 10)):
            tags.append(choice(Tag.objects.all()))
        teaser = '\n\n'.join(fake.paragraphs(randint(1, 3)))
        content = '\n\n'.join(fake.paragraphs(randint(3, 10)))
        content_prev = '\n\n'.join(fake.paragraphs(randint(3, 10)))
        if not Post.exist(slug):
            p = Post.objects.create(
                slug=slug,
                title=title,
                author=author,
                description=description,
                keywords=keywords,
                status=status,
                sticked=sticked,
                comments_enabled=comments_enabled,
                comments_moderated=comments_moderated,
                do_ping=do_ping,
                published=published,
                teaser=teaser,
                content=content,
                content_prev=content_prev
            )
            p.save()
            for c in categories:
                if c not in p.categories.all():
                    p.categories.add(c)
            for t in tags:
                if t not in p.tags.all():
                    p.tags.add(t)
            print(p)


def blog_comment(post, parent=None):
    if randint(0, 1):
        fake = fake_ru
    else:
        fake = fake_en
    c = Comment.objects.create(
        post=post,
        username=fake.name(),
        email=fake.email(),
        agent=fake.user_agent(),
        ip=fake.ipv4(),
        content='\n\n'.join(fake.paragraphs(randint(1, 3)))
    )
    c.save()
    if parent is None:
        c.path = str(c.id)
    else:
        c.path = parent.path + '-' + str(c.id)
    c.save()
    print(c)


def blog_comments():
    posts = Post.objects.all()
    for post in posts:
        for _ in range(0, randint(10, 20)):
            blog_comment(post)


def blog_subcomments():
    comments = Comment.objects.all()
    for _ in range(0, int(comments.count()/3)):
        c = choice(comments)
        for _ in range(0, randint(0, 2)):
            blog_comment(c.post, c)


class Command(BaseCommand):
    help = 'generate random data'

    def handle(self, **options):
        clean()
        blog_category(5)
        blog_tag(25)
        blog_post(20)
        blog_comments()
        blog_subcomments()
        blog_subcomments()
        blog_subcomments()
        blog_subcomments()
        links_mylink()
