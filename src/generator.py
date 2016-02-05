import random
from project import db
from project.auth.models import User
from project.blog.models import Tag, Category
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

for _ in range(0, 100):
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
            tagname=name
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
            categoryname=name
        )
        c.order = order
        db.session.add(c)
        print(c)
    else:
        print('category is exist: ' + name)


print('COMMIT')
db.session.commit()
