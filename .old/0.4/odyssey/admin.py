from django.contrib.admin import *  # PART 1

class MyAdminSite(AdminSite):
    site_header = "My Site"

    def __init__(self, *args, **kwargs):
        super(MyAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(site._registry)  # PART 2

admin_site = MyAdminSite()
