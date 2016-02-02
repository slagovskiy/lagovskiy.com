from django.db import models
from apps.blog.models import Post

class PingServer(models.Model):
    PING_PAGE = 1
    PING_RSS = 2
    PING_TYPE = (
        (PING_PAGE, '1'),
        (PING_RSS, '2'),
    )
    address = models.CharField(max_length=255, verbose_name=u'Address',)
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted',)
    type = models.IntegerField(choices=PING_TYPE, default=1, verbose_name='Type',)

    def __unicode__(self):
        return self.address

    class Meta:
        ordering = ['address']

class PingResult(models.Model):
    date = models.DateField(auto_now=True, auto_now_add=True)
    time = models.TimeField(auto_now=True, auto_now_add=True)
    pingserver = models.ForeignKey(PingServer, null=True, blank=True)
    post = models.ForeignKey(Post, null=True, blank=True)
    passed = models.BooleanField(default=False)
    message = models.CharField(max_length=255, default='')

    def __unicode__(self):
        return '%s %s' %(self.date, str(self.passed))