import random
from datetime import datetime
from project import db
from project.auth.models import User
from project.blog.models import Tag, Category, Post
from project.links.models import MyLink
from faker import Factory


fake_ru = Factory.create('ru-RU')
fake_en = Factory.create('en-US')

print('CLEAR DATABASE')
db.drop_all()

print('CREATE TABLES')
db.create_all()

print('\nGENERATE USERS')
u = User(
    username='sergey',
    email='sergey@lagovskiy.com',
    password='123'
)
u.role = 0
db.session.add(u)
print('USER: Sergey')

for _ in range(0, 10):
    username = fake_en.first_name().lower()
    email = username + '@' + fake_en.free_email_domain()
    password = '123'
    if (not User.username_exist(username)) and (not User.email_exist(email)):
        u = User(
            username=username,
            email=email,
            password=password
        )
        db.session.add(u)
        print(u)
    else:
        print('user or email is exist: ' + username + ' [' + email + ']')

print('\nGENERATE TAGS')
for _ in range(0, 50):
    slug = fake_en.slug()
    name = ''
    if random.randint(0, 1) == 0:
        name = fake_en.word()
    else:
        name = fake_ru.word()
    if not Tag.exist(slug):
        t = Tag(
            slug=slug,
            name=name
        )
        db.session.add(t)
        print(t)
    else:
        print('tag is exist: ' + name)

print('\nGENERATE CATEGORIES')
for _ in range(0, 10):
    slug = fake_en.slug()
    order = random.randint(0, 100)
    name = ''
    if random.randint(0, 1) == 0:
        name = fake_en.word()
    else:
        name = fake_ru.word()
    if not Category.exist(slug):
        c = Category(
            slug=slug,
            name=name
        )
        c.order = order
        db.session.add(c)
        print(c)
    else:
        print('category is exist: ' + name)


print('\nGENERATE MYLINKS')
slug = 'facebook'
name = '<i class="fa fa-facebook-official"></i> i on facebook'
link = 'https://www.facebook.com/sergey.lagovskiy'
ml = MyLink(
    slug=slug,
    name=name,
    link=link
)
db.session.add(ml)
print(ml)
slug = 'flickr'
name = '<i class="fa fa-flickr"></i>  my photos on flickr'
link = 'https://www.flickr.com/photos/slagovskiy/'
ml = MyLink(
    slug=slug,
    name=name,
    link=link
)
db.session.add(ml)
print(ml)
slug = 'github'
name = '<i class="fa fa-github-square"></i> my code on github'
link = 'https://github.com/slagovskiy'
ml = MyLink(
    slug=slug,
    name=name,
    link=link
)
db.session.add(ml)
print(ml)
slug = 'email'
name = '<i class="fa fa-envelope-square"></i> write me email'
link = 'mailto:slagovskiy@gmail.com'
blank = False
ml = MyLink(
    slug=slug,
    name=name,
    link=link,
    blank=blank
)
db.session.add(ml)
print(ml)
slug = 'hh'
name = '<i class="fa fa-user"></i> headhunt me'
link = 'http://novosibirsk.hh.ru/resume/4f27274aff01958a560039ed1f7a44564d3256'
ml = MyLink(
    slug=slug,
    name=name,
    link=link
)
db.session.add(ml)
print(ml)

print('COMMIT')
db.session.commit()


for _ in range(0, 100):
    fake = None
    if random.randint(0, 1) == 0:
        fake = fake_en
    else:
        fake = fake_ru
    p = Post()
    p.author = random.choice(User.query.all())
    for i in range(0, random.randint(1, 10)):
        p.tags.append(random.choice(Tag.query.all()))
    for i in range(0, random.randint(1, 3)):
        p.categories.append(random.choice(Category.query.all()))
    p.status = random.randint(0, 2)
    p.template = random.randint(1, 6)
    title = ''
    teaser = ''
    content = ''
    slug = fake_en.slug()
    _title = fake.words(random.randint(2, 6))
    for i in range(0, len(_title)):
            title += _title[i] + ' '
    title = title[0:1].upper() + title[1:]
    for i in range(0, random.randint(1, 2)):
        teaser += '<p>' + fake.paragraph() + '</p>\n'
    for i in range(0, random.randint(1, 7)):
        content += '<p>' + fake.paragraph() + '</p>\n'
    p.slug = slug
    p.title = title
    p.teaser = teaser
    p.content = content
    p.published = datetime.utcnow()
    db.session.add(p)
    print(p)

print('COMMIT')
db.session.commit()
