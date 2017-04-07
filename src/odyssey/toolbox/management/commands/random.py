from random import randint, choice
from ....blog.models import Tag, Category, Post, Comment
from ....photo.models import Photo, Album, Tag as PhotoTag
from ....userext.models import User
from ...models import PingServer
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker.factory import Factory
from ....links.models import MyLink
from ....settings import MEDIA_ROOT

from django.core.files import File
import urllib.request
import os
import uuid


fake_ru = Factory.create('ru-RU')
fake_en = Factory.create('en-US')
fake = None


def clean():
    MyLink.objects.all().delete()
    Post.objects.all().delete()
    Comment.objects.all().delete()
    Tag.objects.all().delete()
    Category.objects.all().delete()
    PingServer.objects.all().delete()
    Album.objects.all().delete()
    PhotoTag.objects.all().delete()
    Photo.objects.all().delete()
    for root, dirs, files in os.walk(os.path.join(MEDIA_ROOT, 'photo'), topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def pingserver():
    data = '''http://ping.blogs.yandex.ru/RPC2
http://blogsearch.google.com/ping/RPC2'''
    data1 = '''http://1470.net/api/ping
http://a2b.cc/setloc/bp.a2b
http://api.feedster.com/ping
http://api.moreover.com/ping
http://api.moreover.com/RPC2
http://api.mw.net.tw/RPC2
http://api.my.yahoo.co.jp/RPC2
http://api.my.yahoo.com/ping
http://api.my.yahoo.com/RPC2
http://api.my.yahoo.com/rss/ping
http://audiorpc.weblogs.com/RPC2
http://bblog.com/ping.php
http://bblog.comping.php
http://bitacoles.net/notificacio.php
http://bitacoles.net/ping.php
http://bitacoras.net/ping
http://bitacoras.net/ping/
http://blo.gs/ping.php
http://blog.goo.ne.jp
http://blog.goo.ne.jp/XMLRPC
http://blog.with2.net/ping.php
http://blogbot.dk/io/xml-rpc.php
http://blogdb.jp
http://blogdb.jp/xmlrpc
http://blogdigger.com/RPC2
http://blogmatcher.com/u.php
http://blogoole.com/ping
http://blogoole.com/ping/
http://blogoon.net/ping
http://blogoon.net/ping/
http://blogpeople.net/ping
http://blogping.unidatum.com/RPC2/
http://blogroots.com/tb_populi.blog?id=1
http://blogsdominicanos.com/ping
http://blogsearch.google.ae/ping/RPC2
http://blogsearch.google.at/ping/RPC2
http://blogsearch.google.be/ping/RPC2
http://blogsearch.google.bg/ping/RPC2
http://blogsearch.google.ca/ping/RPC2
http://blogsearch.google.ch/ping/RPC2
http://blogsearch.google.cl/ping/RPC2
http://blogsearch.google.co.cr/ping/RPC2
http://blogsearch.google.co.hu/ping/RPC2
http://blogsearch.google.co.id/ping/RPC2
http://blogsearch.google.co.il/ping/RPC2
http://blogsearch.google.co.in/ping/RPC2
http://blogsearch.google.co.it/ping/RPC2
http://blogsearch.google.co.jp/ping/RPC2
http://blogsearch.google.co.ma/ping/RPC2
http://blogsearch.google.co.nz/ping/RPC2
http://blogsearch.google.co.th/ping/RPC2
http://blogsearch.google.co.uk/ping/RPC2
http://blogsearch.google.co.uk/pingRPC2
http://blogsearch.google.co.ve/ping/RPC2
http://blogsearch.google.co.za/ping/RPC2
http://blogsearch.google.com.ar/ping/RPC2
http://blogsearch.google.com.au/ping/RPC2
http://blogsearch.google.com.br/ping/RPC2
http://blogsearch.google.com.co/ping/RPC2
http://blogsearch.google.com.do/ping/RPC2
http://blogsearch.google.com.mx/ping/RPC2
http://blogsearch.google.com.my/ping/RPC2
http://blogsearch.google.com.pe/ping/RPC2
http://blogsearch.google.com.sa/ping/RPC2
http://blogsearch.google.com.sg/ping/RPC2
http://blogsearch.google.com.tr/ping/RPC2
http://blogsearch.google.com.tw/ping/RPC2
http://blogsearch.google.com.ua/ping/RPC2
http://blogsearch.google.com.uy/ping/RPC2
http://blogsearch.google.com.vn/ping/RPC2
http://blogsearch.google.com/ping/RPC2
http://blogsearch.google.de/ping/RPC2
http://blogsearch.google.es/ping/RPC2
http://blogsearch.google.fi/ping/RPC2
http://blogsearch.google.fr/ping/RPC2
http://blogsearch.google.gr/ping/RPC2
http://blogsearch.google.hr/ping/RPC2
http://blogsearch.google.ie/ping/RPC2
http://blogsearch.google.in/ping/RPC2
http://blogsearch.google.it/ping/RPC2
http://blogsearch.google.jp/ping/RPC2
http://blogsearch.google.lt/ping/RPC2
http://blogsearch.google.nl/ping/RPC2
http://blogsearch.google.pl/ping/RPC2
http://blogsearch.google.pt/ping/RPC2
http://blogsearch.google.ro/ping/RPC2
http://blogsearch.google.ru/ping/RPC2
http://blogsearch.google.se/ping/RPC2
http://blogsearch.google.sk/ping/RPC2
http://blogsearch.google.tw/ping/RPC2
http://blogsearch.google.us/ping/RPC2
http://blogshares.com/rpc.php
http://blogsnow.com/ping
http://blogstreet.com/xrbin/xmlrpc.cgi
http://blogupdate.org/ping/
http://blogupdate.org/sverige/ping/
http://bulkfeeds.net
http://bulkfeeds.net/rpc
http://catapings.com/ping.php
http://coreblog.org/ping
http://coreblog.org/ping/
http://cullect.com/feed/ping
http://effbot.org/rpc/ping.cgi
http://feedsky.com/api/RPC2
http://fgiasson.com/pings/ping.php
http://focuslook.com/ping
http://geourl.org/ping
http://hamo-search.com/ping.php
http://holycowdude.com/rpc/ping
http://holycowdude.com/rpc/ping/
http://imblogs.net/ping
http://imblogs.net/ping/
http://ipings.com
http://j-ranking.com/ping.cgi
http://lasermemory.com/lsrpc
http://lasermemory.com/lsrpc/
http://mod-pubsub.org
http://mod-pubsub.org/kn_apps/blogchatt
http://mod-pubsub.org/knapps/blogchatt
http://mod-pubsub.org/ping.php
http://newsblog.jungleboots.org/ping.php
http://newsisfree.com/RPCCloud
http://packetmonster.net/xmlrpc.php
http://ping.amagle.com
http://ping.amagle.com/
http://ping.bitacoras.com
http://ping.blo.gs
http://ping.blo.gs/
http://ping.blogg.de
http://ping.blogg.de/
http://ping.bloggers.jp/rpc
http://ping.bloggers.jp/rpc/
http://ping.blogmura.jp/rpc/
http://ping.blogoon.net/
http://ping.blogs.yandex.ru/RPC2
http://ping.cocolog-nifty.com/xmlrpc
http://ping.exblog.jp/xmlrpc
http://ping.fakapster.com/rpc
http://ping.fc2.com/
http://ping.feedburner.com
http://ping.feeds.yahoo.com/RPC2/
http://ping.gpost.info/xmlrpc
http://ping.kutsulog.net/
http://ping.myblog.jp
http://ping.namaan.net/rpc
http://ping.rootblog.com/rpc.php
http://ping.snap.com/ping/RPC2
http://ping.speenee.com/xmlrpc
http://ping.syndic8.com/xmlrpc.php
http://ping.weblogalot.com/rpc.php
http://ping.weblogs.se
http://ping.weblogs.se/
http://ping.wordblog.de
http://ping.wordblog.de/
http://pinger.blogflux.com/rpc
http://pinger.onejavastreet.com
http://pingoat.com/
http://pingoat.com/goat/RPC2
http://pingqueue.com/rpc
http://pingqueue.com/rpc/
http://popdex.com/addsite.php
http://queerfilter.com/ping
http://r.hatena.ne.jp/rpc
http://rcs.datashed.net
http://rcs.datashed.net/RPC2
http://rcs.datashed.net/RPC2/
http://rpc.blogbuzzmachine.com/RPC2
http://rpc.bloggerei.de/ping/
http://rpc.blogrolling.com/pinger
http://rpc.blogrolling.com/pinger/
http://rpc.britblog.com
http://rpc.britblog.com/
http://rpc.icerocket.com:10080
http://rpc.icerocket.com:10080/
http://rpc.newsgator.com
http://rpc.newsgator.com/
http://rpc.pingomatic.com
http://rpc.reader.livedoor.com/ping
http://rpc.tailrank.com/feedburner/RPC2
http://rpc.technorati.com/rpc/ping
http://rpc.technorati.jp/rpc/ping
http://rpc.twingly.com
http://rpc.weblogs.com/RPC2
http://rpc.wpkeys.com
http://rssfeeds.com/suggest_wizzard.php
http://rssfwd.com/xmlrpc/api
http://serenebach.net/rep.cgi
http://services.newsgator.com/ngws/xmlrpcping.aspx
http://signup.alerts.msn.com/alerts-PREP/submitPingExtended.doz
http://snipsnap.org/RPC2
http://syndic8.com/xmlrpc.php
http://thingamablog.sourceforge.net/ping.php
http://topicexchange.com
http://topicexchange.com/RPC2
http://trackback.bakeinu.jp/bakeping.php
http://wasalive.com/ping
http://wasalive.com/ping/
http://weblogues.com/ping/
http://weblogues.com/RPC
http://weblogues.com/RPC/
http://www.a2b.cc
http://www.a2b.cc/setloc/bp.a2b
http://www.bitacoles.net/ping.php
http://www.blogdigger.com/RPC2
http://www.bloglines.com/ping
http://www.blogoole.com/ping/
http://www.blogoon.net/ping
http://www.blogoon.net/ping/
http://www.blogpeople.net
http://www.blogpeople.net/servlet/weblogUpdates
http://www.blogroots.com
http://www.blogroots.com/tb_populi.blog?id=1
http://www.blogroots.com/tbpopuli.blog?id=1
http://www.blogsdominicanos.com/ping/
http://www.blogshares.com/rpc.php
http://www.blogsnow.com/ping
http://www.blogstreet.com/xrbin/xmlrpc.cgi
http://www.catapings.com/ping.php
http://www.feedsky.com/api/RPC2
http://www.feedsubmitter.com
http://www.holycowdude.com/rpc/ping/
http://www.imblogs.net/ping/
http://www.lasermemory.com
http://www.lasermemory.com/lsrpc
http://www.lasermemory.com/lsrpc/
http://www.mod-pubsub.org/kn_apps/blogchatter/ping.php
http://www.mod-pubsub.org/knapps/blogchatter/ping.php
http://www.mod-pubsub.org/ping.php
http://www.newsisfree.com/RPCCloud
http://www.newsisfree.com/xmlrpctest.php
http://www.octora.com/add_rss.php
http://www.pingerati.net
http://www.pingmyblog.com
http://www.popdex.com
http://www.popdex.com/addsite.php
http://www.snipsnap.org
http://www.snipsnap.org/RPC2
http://www.wasalive.com/ping/
http://www.weblogalot.com/ping
http://www.weblogues.com
http://www.weblogues.com/RPC
http://www.weblogues.com/RPC/
http://www.xianguo.com/xmlrpc/ping.php
http://www.zhuaxia.com/rpc/server.php
http://xianguo.com/xmlrpc/ping.php
http://xmlrpc.blogg.de
http://xping.pubsub.com/ping
http://xping.pubsub.com/ping/
http://zhuaxia.com/rpc/server.php
http://zing.zingfast.com
http://blogpeople.net/servlet/weblogUpdates
http://ping.kutsulog.net
http://ping.fc2.com
http://ping.blogoon.net
http://mod-pubsub.org/kn_apps/blogchatter/ping.php
http://newsisfree.com/xmlrpctest.php
http://ping.blogmura.jp/rpc
http://blogsearch.google.com/pingRPC2
http://blogsearch.google.com/pingRPC2nd
http://blogsearch.google.us/pingRPC2
http://focuslook.com/ping.php
http://weblogalot.com/ping
http://focuslook.com/ping
http://rpc.weblogs.com/RPC2
http://blogpeople.net/ping
http://audiorpc.weblogs.com/RPC2
http://ping.blogs.yandex.ru/RPC2
http://blogsearch.google.com/ping/RPC2
http://blogsearch.google.ae/ping/RPC2
http://blogsearch.google.at/ping/RPC2
http://blogsearch.google.be/ping/RPC2
http://blogsearch.google.bg/ping/RPC2
http://blogsearch.google.ch/ping/RPC2
http://blogsearch.google.cl/ping/RPC2
http://blogsearch.google.co.id/ping/RPC2
http://blogsearch.google.co.il/ping/RPC2
http://blogsearch.google.co.in/ping/RPC2
http://blogsearch.google.co.jp/ping/RPC2
http://blogsearch.google.co.ma/ping/RPC2
http://blogsearch.google.co.nz/ping/RPC2
http://blogsearch.google.co.th/ping/RPC2
http://blogsearch.google.co.uk/ping/RPC2
http://blogsearch.google.co.ve/ping/RPC2
http://blogsearch.google.co.za/ping/RPC2
http://blogsearch.google.com.ar/ping/RPC2
http://blogsearch.google.com.au/ping/RPC2
http://blogsearch.google.com.br/ping/RPC2
http://blogsearch.google.com.co/ping/RPC2
http://blogsearch.google.com.mx/ping/RPC2
http://blogsearch.google.com.my/ping/RPC2
http://blogsearch.google.com.pe/ping/RPC2
http://blogsearch.google.com.sa/ping/RPC2
http://blogsearch.google.com.sg/ping/RPC2
http://blogsearch.google.com.tr/ping/RPC2
http://blogsearch.google.com.tw/ping/RPC2
http://blogsearch.google.com.ua/ping/RPC2
http://blogsearch.google.com.uy/ping/RPC2
http://blogsearch.google.com.vn/ping/RPC2
http://blogsearch.google.de/ping/RPC2
http://blogsearch.google.es/ping/RPC2
http://blogsearch.google.fi/ping/RPC2
http://blogsearch.google.fr/ping/RPC2
http://blogsearch.google.gr/ping/RPC2
http://blogsearch.google.hr/ping/RPC2
http://blogsearch.google.ie/ping/RPC2
http://blogsearch.google.it/ping/RPC2
http://blogsearch.google.jp/ping/RPC2
http://blogsearch.google.lt/ping/RPC2
http://blogsearch.google.nl/ping/RPC2
http://blogsearch.google.pl/ping/RPC2
http://blogsearch.google.pt/ping/RPC2
http://blogsearch.google.ro/ping/RPC2
http://blogsearch.google.ru/ping/RPC2
http://blogsearch.google.se/ping/RPC2
http://blogsearch.google.sk/ping/RPC2
http://blogsearch.google.us/ping/RPC2
http://blogpeople.net/servlet/weblogUpdates
http://blogsearch.google.ca/ping/RPC2
http://blogsearch.google.co.cr/ping/RPC2
http://blogsearch.google.co.hu/ping/RPC2
http://blogsearch.google.com.do/ping/RPC2
http://blogpingr.de/ping/rpc2
http://i-learn.jp/ping/
http://rpc.bloggerei.de/ping/
http://www.blogpeople.net/servlet/weblogUpdates
http://xping.pubsub.com/ping/
http://ping.pubsub.com/ping
http://www.blogpeople.net/ping
http://xping.pubsub.com/ping
http://pingomatic.com/
http://blogsearch.google.lk/ping/RPC2
http://blogsearch.google.ws/ping/RPC2
http://blogsearch.google.vu/ping/RPC2
http://blogsearch.google.vg/ping/RPC2
http://blogsearch.google.tt/ping/RPC2
http://blogsearch.google.tp/ping/RPC2
http://blogsearch.google.to/ping/RPC2
http://blogsearch.google.tm/ping/RPC2
http://blogsearch.google.tl/ping/RPC2
http://blogsearch.google.tk/ping/RPC2
http://blogsearch.google.st/ping/RPC2
http://blogsearch.google.sn/ping/RPC2
http://blogsearch.google.sm/ping/RPC2
http://blogsearch.google.si/ping/RPC2
http://blogsearch.google.sh/ping/RPC2
http://blogsearch.google.sc/ping/RPC2
http://blogsearch.google.rw/ping/RPC2
http://blogsearch.google.pn/ping/RPC2
http://blogsearch.google.nu/ping/RPC2
http://blogsearch.google.nr/ping/RPC2
http://blogsearch.google.no/ping/RPC2
http://blogsearch.google.mw/ping/RPC2
http://blogsearch.google.mv/ping/RPC2
http://blogsearch.google.mu/ping/RPC2
http://blogsearch.google.ms/ping/RPC2
http://blogsearch.google.mn/ping/RPC2
http://blogsearch.google.md/ping/RPC2
http://blogsearch.google.lu/ping/RPC2
http://blogsearch.google.li/ping/RPC2
http://blogsearch.google.la/ping/RPC2
http://blogsearch.google.kz/ping/RPC2
http://blogsearch.google.ki/ping/RPC2
http://blogsearch.google.kg/ping/RPC2
http://blogsearch.google.jo/ping/RPC2
http://blogsearch.google.je/ping/RPC2
http://blogsearch.google.is/ping/RPC2
http://blogsearch.google.im/ping/RPC2
http://blogsearch.google.hu/ping/RPC2
http://blogsearch.google.ht/ping/RPC2
http://blogsearch.google.hn/ping/RPC2
http://blogsearch.google.gy/ping/RPC2
http://blogsearch.google.gp/ping/RPC2
http://blogsearch.google.gm/ping/RPC2
http://blogsearch.google.gl/ping/RPC2
http://blogsearch.google.gg/ping/RPC2
http://blogsearch.google.ge/ping/RPC2
http://blogsearch.google.fm/ping/RPC2
http://blogsearch.google.ee/ping/RPC2
http://blogsearch.google.dm/ping/RPC2
http://blogsearch.google.dk/ping/RPC2
http://blogsearch.google.dj/ping/RPC2
http://blogsearch.google.cz/ping/RPC2
http://blogsearch.google.cn/ping/RPC2
http://blogsearch.google.ci/ping/RPC2
http://blogsearch.google.cg/ping/RPC2
http://blogsearch.google.cd/ping/RPC2
http://blogsearch.google.bs/ping/RPC2
http://blogsearch.google.bi/ping/RPC2
http://blogsearch.google.ba/ping/RPC2
http://blogsearch.google.az/ping/RPC2
http://blogsearch.google.as/ping/RPC2
http://blogsearch.google.am/ping/RPC2
http://blogsearch.google.ad/ping/RPC2
http://blogsearch.google.com.vc/ping/RPC2
http://blogsearch.google.com.tj/ping/RPC2
http://blogsearch.google.com.sv/ping/RPC2
http://blogsearch.google.com.sb/ping/RPC2
http://blogsearch.google.com.qa/ping/RPC2
http://blogsearch.google.com.py/ping/RPC2
http://blogsearch.google.com.pr/ping/RPC2
http://blogsearch.google.com.pk/ping/RPC2
http://blogsearch.google.com.ph/ping/RPC2
http://blogsearch.google.com.pa/ping/RPC2
http://blogsearch.google.com.om/ping/RPC2
http://blogsearch.google.com.np/ping/RPC2
http://blogsearch.google.com.ni/ping/RPC2
http://blogsearch.google.com.ng/ping/RPC2
http://blogsearch.google.com.nf/ping/RPC2
http://blogsearch.google.com.na/ping/RPC2
http://blogsearch.google.com.mt/ping/RPC2
http://www.blogsearch.google.se/ping/RPC2
http://www.blogsearch.google.sk/ping/RPC2
http://www.blogsearch.google.us/ping/RPC2
http://ping.rss.drecom.jp
http://rpc.weblogs.com/RPC2
'''
    for s in data.split('\n'):
        if s != '':
            p = PingServer.objects.create(
                address=s,
                deleted=False
            )
            p.save()
            print(p)

def links_mylink():
    slug = 'facebook'
    name = '<i class="fa fa-facebook-official"></i> i\'m on facebook'
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
            print('%s:%s %s' % (_, count, t))


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
                content=content
            )
            p.save()
            for c in categories:
                if c not in p.categories.all():
                    p.categories.add(c)
            for t in tags:
                if t not in p.tags.all():
                    p.tags.add(t)
            print('%s:%s %s' % (_, count, p))


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


def blog_comments():
    posts = Post.objects.all()
    c = 0
    for post in posts:
        cnt = randint(5, 10)
        for _ in range(0, cnt):
            blog_comment(post)
            print('%s:%s %s:%s comment for %s' % (c, len(posts), _, cnt, post))
        c += 1



def blog_subcomments():
    comments = Comment.objects.all()
    cntt = int(comments.count()/3)
    cc = 0
    for _ in range(0, cntt):
        c = choice(comments)
        cnt = randint(0, 2)
        for _ in range(0, cnt):
            blog_comment(c.post, c)
            print('%s:%s: %s:%s subcomment for %s' % (cc, cntt, _, cnt, c.post))
        cc += 1


def photo_tag(count):
    for _ in range(0, count):
        if randint(0, 1):
            fake = fake_ru
        else:
            fake = fake_en
        slug = fake.slug()
        name = fake.word()
        if not PhotoTag.exist(slug):
            t = PhotoTag.objects.create(
                slug=slug,
                name=name
            )
            t.save()
            print('%s:%s %s' % (_, count, t))


def photo_album(count):
    for _ in range(0, count):
        if randint(0, 1):
            fake = fake_ru
        else:
            fake = fake_en
        slug = fake.slug()
        name = fake.word()
        if not Album.exist(slug):
            a = Album.objects.create(
                slug=slug,
                name=name,
                order=randint(1, 100)
            )
            a.save()
            print('%s:%s %s' % (_, count, a))

def photo(count):
    for _ in range(0, count):
        if randint(0, 1):
            fake = fake_ru
        else:
            fake = fake_en
        slug = fake.slug()
        uid = str(uuid.uuid1())
        if not os.path.exists(os.path.join(MEDIA_ROOT, 'photo')):
            os.mkdir(os.path.join(MEDIA_ROOT, 'photo'))
        if not os.path.exists(os.path.join(os.path.join(MEDIA_ROOT, 'photo'), uid)):
            os.mkdir(os.path.join(os.path.join(MEDIA_ROOT, 'photo'), uid))
        path = os.path.join(os.path.join(os.path.join(MEDIA_ROOT, 'photo'), uid), 'image.jpg')
        title = ' '.join(fake.words(randint(1, 6)))
        title = title[0:1].upper() + title[1:]
        author = User.objects.all().first()
        status = randint(0, 2)
        sticked = False
        if randint(0, 1):
            sticked = True
        published = None
        if status == 2:
            published = timezone.now()
        albums = []
        for __ in range(1, randint(2, 4)):
            albums.append(choice(Album.objects.all()))
        tags = []
        for __ in range(1, randint(1, 10)):
            tags.append(choice(PhotoTag.objects.all()))
        url = 'http://lorempixel.com/%s/%s/' % (str(randint(300, 800)), str(randint(300, 800)))
        urllib.request.urlretrieve(url, path)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            p = Photo.objects.create(
                slug=slug,
                title=title,
                author=author,
                status=status,
                sticked=sticked,
                published=published,
                image=path
            )
            p.save()
            for a in albums:
                if a not in p.albums.all():
                    p.albums.add(a)
            for t in tags:
                if t not in p.tags.all():
                    p.tags.add(t)
            print('%s:%s %s' % (_, count, p))



class Command(BaseCommand):
    help = 'generate random data'

    def handle(self, **options):
        clean()
        pingserver()
        blog_category(5)
        blog_tag(50)
        blog_post(150)
        blog_comments()
        blog_subcomments()
        blog_subcomments()
        blog_subcomments()
        links_mylink()
        photo_album(10)
        photo_tag(50)
        photo(500)
