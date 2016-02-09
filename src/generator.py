import os
import random
from PIL import Image, ImageDraw
from uuid import uuid4
from datetime import datetime
from project import db
from config import UPLOAD_DIR
from project.auth.models import User
from project.blog.models import Tag, Category, Post
from project.links.models import MyLink
from project.media.models import MediaFolder, MediaFile
from faker import Factory


fake_ru = Factory.create('ru-RU')
fake_en = Factory.create('en-US')


def drawImage(x=300, y=200):
    testImage = Image.new("RGB", (x, y), (255, 255, 255))
    pixel = testImage.load()
    draw = ImageDraw.Draw(testImage)
    for _ in range(100, random.randint(200, 500)):
        red1 = random.randrange(0, 255)
        blue1 = random.randrange(0, 255)
        green1 = random.randrange(0, 255)
        red2 = random.randrange(0, 255)
        blue2 = random.randrange(0, 255)
        green2 = random.randrange(0, 255)
        draw.ellipse(
            (random.randint(1, x-1), random.randint(1, x-1), random.randint(1, y-1), random.randint(1, y-1)),
            fill=(red1, blue1, green1), outline=(red2, blue2, green2)
        )
    for _ in range(100, random.randint(200, 1000)):
        red = random.randrange(0, 255)
        blue = random.randrange(0, 255)
        green = random.randrange(0, 255)
        pixel[random.randint(1, x-1), random.randint(1, y-1)] = (red, blue, green)
    return testImage

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

print('\nGENERATE MEDIAFOLDERS')
for user in User.query.all():
    for _ in range(0, random.randint(1, 20)):
        fake = None
        if random.randint(0, 1) == 0:
            fake = fake_en
        else:
            fake = fake_ru
        mf = MediaFolder(
            name=fake.word()
        )
        mf.author = user
        db.session.add(mf)
        print(mf)

print('\nGENERATE FILES')
for folder in MediaFolder.query.all():
    for _ in range(0, random.randint(1, 20)):
        fake = None
        if random.randint(0, 1) == 0:
            fake = fake_en
        else:
            fake = fake_ru
        mf = MediaFile(
            uuid=str(uuid4()),
            name=fake.word(),
            ext='png',
            folder=folder
        )
        mf.author = folder.author
        db.session.add(mf)
        print(mf)

mf_count = MediaFile.query.count()
mf_i = 0
for mf in MediaFile.query.all():
    file_dir = os.path.join(UPLOAD_DIR, mf.uuid)
    os.mkdir(file_dir)
    img = drawImage(random.randint(50, 1000), random.randint(50, 1000))
    img.save(os.path.join(file_dir, mf.name + '.' + mf.ext))
    mf_i += 1
    print('generated image: %s from %s' % (mf_i, mf_count))


print('\nGENERATE POSTS')
for _ in range(0, 50):
    fake = None
    if random.randint(0, 1) == 0:
        fake = fake_en
    else:
        fake = fake_ru
    title = ''
    teaser = ''
    content = ''
    slug = fake_en.slug()
    if not Post.exist(slug):
        p = Post()
        p.author = random.choice(User.query.all())
        for i in range(0, random.randint(1, 10)):
            p.tags.append(random.choice(Tag.query.all()))
        for i in range(0, random.randint(1, 3)):
            p.categories.append(random.choice(Category.query.all()))
        p.status = random.randint(0, 2)
        p.template = random.randint(1, 6)
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
