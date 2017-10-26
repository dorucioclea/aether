from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from gather2.common.auth.views import obtain_auth_token


auth_urls = 'rest_framework.urls'
if settings.CAS_SERVER_URL:  # pragma: no cover
    import django_cas_ng.views

    auth_urls = [
        url(r'^login/$', django_cas_ng.views.login, name='login'),
        url(r'^logout/$', django_cas_ng.views.logout, name='logout'),
    ]

urlpatterns = [
    url(r'', include('gather2.core.api.urls')),
    url(r'^v1/', include('gather2.core.api.urls', namespace='v1')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(auth_urls, namespace='rest_framework')),
    url(r'^accounts/token', obtain_auth_token, name='token'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:  # pragma: no cover
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
