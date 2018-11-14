from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/users/$', views.UserCreate.as_view(), name='account-create'),
    url(r'^api/v1/auth/login/$', views.LoginView.as_view(), name='Login'),
    url(r'^api/v1/auth/logout/$', views.LogoutView.as_view(), name='Logout'),
]