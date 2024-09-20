from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_post/', views.new_post, name='new_post'),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.follow_unfollow_user, name="follow_unfollow"),
    path('following', views.following, name='following'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)