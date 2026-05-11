import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path

from trend_in_bulk_app.sitemap import StaticViewSitemap

handler404 = "trend_in_bulk_app.views.page_not_found"

sitemaps = {
    "static": StaticViewSitemap,
}


def robots_txt(request):
    file_path = os.path.join(settings.BASE_DIR, "trend_in_bulk_pro", "robots.txt")
    with open(file_path, "r") as file:
        return HttpResponse(file.read(), content_type="text/plain")


urlpatterns = [
    path("", include("trend_in_bulk_app.urls")),
    path("robots.txt", robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
