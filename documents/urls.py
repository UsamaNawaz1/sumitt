from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('terms', views.terms, name='terms'),
    path('privacy-policy', views.policy, name='policy'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('documents', views.documents, name='documents'),
    path('documents/add', views.document_add, name='document_add'), #for updating linkedin profile info
    path('summarize/<int:document_id>', views.summarize, name='summarize'), #for updating linkedin profile info
    path('summarize/<int:document_id>/<int:sentences>', views.summarize, name='summarize'), #for updating linkedin profile info
    path('documents/edit/<int:document_id>', views.document_edit, name='document_edit'), #for updating linkedin profile info
    path('documents/delete/<int:document_id>', views.document_delete, name='document_delete'), #for updating linkedin profile info
    path('staff/users', views.users, name='admin_users'),
    path('staff/documents', views.admin_documents, name='admin_documents'),
    # path('campaign/<int:campaign_id>/messages', views.campaign_messages, name='message'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
