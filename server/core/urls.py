from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # API endpoints
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),

    # Auto-generated DRF docs
    # http://www.django-rest-framework.org/topics/documenting-your-api/
    url(r'^docs/', include_docs_urls(
        title='Spare',
        public=True,
        authentication_classes=[],
        permission_classes=[],
    )),

    # Django RQ
    url(r'^django-rq/', include('django_rq.urls')),

    # Grappeli admin
    url(r'^grappelli/', include('grappelli.urls')),
]
urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls))
    )
