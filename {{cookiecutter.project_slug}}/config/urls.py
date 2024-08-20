from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
{%- if cookiecutter.use_async == 'y' %}
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
{%- endif %}
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
import apps.file_management.views as file_views
{%- if cookiecutter.use_drf == 'y' %}
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
{%- endif %}
from commons.views import DashboardView
from commons.admin import user_admin_site
from posts.views import PostListView, PostDetailView
from faqs.views import FaqListView
import apps.file_management.views as file_views

urlpatterns = [
    # Public Pages
    path("", PostListView.as_view(), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("faqs/", FaqListView.as_view(), name="faqs"),
    # Admin Home
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # Posts
    path("posts/", include("posts.urls", namespace="posts")),
    # User management
    path("users/registrations/", include("user_registration.urls", namespace="user_registration")),
    path("profile/", include("users.profile_urls", namespace="profile")),
    path("accounts/", include("allauth.urls")),
    # FAQ Management
    path("faqs/manage/", include("faqs.urls", namespace="faqs_management")),
    # Post Management
    path("posts/manage/", include("posts.post_management_urls", namespace="posts_management")),
    # User Management
    path("users/manage/", include("users.user_management_urls", namespace="user_management")),
    # File Management
    path("", include("file_management.urls", namespace="file")),
    # Guidelines
    path("guidelines/", include("guidelines.urls", namespace="guidelines")),
    # Role and Module Management
    path("roles/", include("role_management.urls", namespace="roles")),
    path("modules/", include("module_management.urls", namespace="modules")),
    # History Management
    path("history/ajax/", include("history_management.urls", namespace="history")),
    # Notifications
    path('inbox/notifications/', include("notification_management.urls", namespace='notifications')),
    # Your stuff: custom urls includes go here
    path("roles/", include("role_management.urls", namespace="roles")),
    path("modules/", include("module_management.urls", namespace="modules")),
    # MEDIA ACCESS
    path(f"media/<str:file>", file_views.serve_public_media_view, name="public_media"),
    path(f"internal/media/upload_temp/<str:file>", file_views.serve_temp_media_view, name="temp_media"), #django-formset uploads files in default_storage. See STORAGES. Changed default to InternalFileStorage to protect files
    path(f"internal/media/<str:file>", file_views.serve_internal_media_view, name="internal_media"),
]

# THIRD PARTY LIBRARIES and DEPENDENCIES
urlpatterns += [
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    path(settings.ADMIN_URL, admin.site.urls),
    # https://django-session-security.readthedocs.io/en/latest/quick.html
    path(r'session_security/', include('session_security.urls')),
    # Comments
    path(r'comments/', include('django_comments_xtd.urls')),
    # disabling accounts/email
    path("accounts/email/", default_views.page_not_found, kwargs={"exception": Exception("Page not Found")},),
    # disabling users portfolio to avoid updating of user information
    # path("users/", include("users.urls", namespace="users")),
]
{%- if cookiecutter.use_async == 'y' %}
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()
{%- endif %}
{% if cookiecutter.use_drf == 'y' %}
# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]
{%- endif %}

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    if "hijack" in settings.INSTALLED_APPS:
        urlpatterns += [path('hijack/', include('hijack.urls')),]