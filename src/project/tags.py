from datetime import datetime
from jinja2 import Markup


class tag_datetime(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __init__(self):
        self.timestamp = datetime.utcnow()

    def render(self, format):
        return Markup(self.timestamp.strftime(format))

    def format(self, fmt='%Y/%m/%d %H:%M:%S'):
        return self.render(fmt)
