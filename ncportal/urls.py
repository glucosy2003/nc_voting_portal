from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", include("customadmin.urls")),  # ✅ Your custom admin
    path("", include("vote.urls")),  # ✅ Voting portal
    path('login/', auth_views.LoginView.as_view(template_name='vote/login.html'), name='login'),
]
# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
