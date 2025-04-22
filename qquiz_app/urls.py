from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from quizzes.views import CustomLogoutView, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quizzes.urls')),
    path('accounts/register/', register, name='register'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)