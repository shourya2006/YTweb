from django import template
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.indexx, name="home"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("sourcecode/", views.sourcecode, name="sourcecode"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("video/<int:myid>", views.video, name="video_page"),
    path("resetpassword/",auth_views.PasswordResetView.as_view(template_name = "Home/password_reset.html"),  name = "password_reset"),
    path("resetpasswordsent/",auth_views.PasswordResetDoneView.as_view(template_name = "Home/password_sent.html"), name = "password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name = "Home/password_change.html"), name = "password_reset_confirm"),
    path("resetpasswordcomplete/",auth_views.PasswordResetCompleteView.as_view(template_name = "Home/password_complete.html") , name = "password_reset_complete"),
    path("search/", views.search, name="search"),
    # path("practice/", views.practice, name="practice"),
    path("practice/python/", views.python, name="python"),
    path("practice/htmlcssjs/", views.html, name="html"),
    path('runcode', views.runcode, name="runcode"),

]
# 