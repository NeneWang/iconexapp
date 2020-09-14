from django.urls import path

# from source.get_involved.views import get_involved_view, application_view
from . import views
from django.views.generic import TemplateView
# path('about/', get_involved_view, name='about'),

urlpatterns = [
    
    # Test
    path('iconex/', views.iconex, name='iconex'),
    path('create_users/', views.createUsers, name='create_users'),
    path('add_token_test/', views.add_token_test, name='add_token_test'),
    path('temporal_method/', views.temporal_method, name='temporal_method'),

    # ICON API
    path('add_token_to_player/', views.add_token_to_player, name='add_token_to_player'),

    # Common
    path('about/', views.about, name='about'),
    path('welcome/', views.index, name='welcome'),
    path('', views.index, name='home'),

    # Not logged in
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),

    path('post_login/', views.post_login, name='post_login'),
    path('post_signup/', views.post_signup, name='post_signup'),

    # Logged in
    path('profile/', views.profile.as_view(), name='profile'),
    path('play/', views.play.as_view(), name='play'),
    path('logout/', views.logout_page, name='logout'),
    
]
