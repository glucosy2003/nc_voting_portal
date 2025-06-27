from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import RegisterView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.student_login, name='student_login'),
    path('login/dashboard/', views.voting_dashboard, name='dashboard'),  # changed here
    path('voter_register/', views.voter_register, name='voter_register'),
    path('vote/<int:candidate_id>/', views.vote, name='vote'),
    path('apply/', RegisterView.as_view(), name='apply'),
    path('about/', views.about_page, name='about'),
    path('results/', views.results_view, name='results'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('help/', views.help_page, name='help_page'), 
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
