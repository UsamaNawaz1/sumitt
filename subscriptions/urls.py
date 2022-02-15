from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('checkout/<int:plan_id>', views.checkout, name='checkout'),
    # path('subscribe', views.checkout, name='subscribe'),
    # # path('linkedin/profile', views.linkedin_profile, name='linkedin_profile'), #for updating linkedin profile info
    # path('linkedin/connections', views.connections, name='connections'),
    # path('linkedin/connections/import', views.connections_import, name='connections_import'),
    # # path('linkedin/connection/edit', views.connections_edit, name='connections_edit'),
    # path('linkedin/profile/edit', views.linkedin_profile_edit, name='linkedin_profile_edit'), #for updating linkedin profile info
    # path('measure', views.measure, name='measure'),
    # path('dashboard', views.dashboard, name='dashboard'),
    # path('campaigns', views.campaigns, name='campaigns'),
    # path('campaigns/add', views.add_campaign, name='add_campaign'),
    # path('campaign/<int:campaign_id>/messages', views.campaign_messages, name='message'),
    # path('updateaccounts', views.updateaccounts, name='updateaccounts'),
    # path('login', views.login_user, name='login'),
    # path('logout', views.logout_user, name='logout'),
    # path('register', views.register_user, name='register'),
    # path('edit_profile', views.edit_profile, name='edit_profile'),
    # path('change_password', views.change_password, name='change_password'),

]
