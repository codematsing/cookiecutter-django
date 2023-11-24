from django.contrib import admin
from django.contrib.admin import AdminSite

# Register your models here.
class UserAdmin(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = 'admin'

    # Text to put in each page's <h1> (and above login form).
    site_header = 'Administration'

    # Text to put at the top of the admin index page.
    index_title = 'Site adminstration'

user_admin_site = UserAdmin()