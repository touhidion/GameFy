from django.conf.urls import url
from . import views

app_name = 'gamefy'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^register/$', views.registration_view, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^game/$', views.game_view, name='game'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^scoreboard/$', views.score_board_view, name='scoreboard'),
    url(r'^404/$', views.error_view, name='error-404'),
    url(r'^delete_gamer/$', views.delete_gamer_view, name='delete_gamer'),
]