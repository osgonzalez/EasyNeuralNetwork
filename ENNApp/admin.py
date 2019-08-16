from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.site_header = "Easy Neural Network"
admin.site.site_title = "ENN"
admin.site.index_title = "User Administration"


admin.site.site_url = "/index"

#admin.site.unregister(Group)


