from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin

from rest_framework.documentation import include_docs_urls

from review import views


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/reviews/", views.ReviewList.as_view()),
    path("api/v1/reviews/<int:pk>/", views.ReviewDetail.as_view()),
    url(r'^docs/', include_docs_urls(title="Review API"))
]


if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:  # pragma: no cover
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
