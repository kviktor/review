from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns

from review import views


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/reviews/", views.ReviewList.as_view()),
    path("api/v1/reviews/<int:pk>/", views.ReviewDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)


if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:  # pragma: no cover
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
