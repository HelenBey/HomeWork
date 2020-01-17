from django.conf.urls import url
from django.contrib import admin

from lab_app.views import FilmView, ListFilmView, AddFilmView, \
    SignUpView, LoginView, LogoutView, CreateReview, AboutView

urlpatterns = [
    url(r'^$', ListFilmView.as_view()),
    url(r'^page=(?P<page>\d+)', ListFilmView.as_view()),
    url(r'^film/(?P<film_id>\d+)', FilmView.as_view()),
    url(r'^create_review/(?P<film_id>\d+)$', CreateReview.as_view()),
    url(r'^film/add_film/$', AddFilmView.as_view()),
    url(r'^signup/$', SignUpView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^about/', AboutView.as_view()),
    url(r'^admin/', admin.site.urls),
]
