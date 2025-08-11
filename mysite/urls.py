from django.contrib import admin
from django.urls import path, include
from accounts import views as acc_views
from django.contrib.auth import views as auth_views
from accounts.views import LoginViewBootstrap, home_redirect
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', home_redirect, name='home'),
        
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('register/', acc_views.register, name='register'),
    path('dashboard/', acc_views.dashboard, name='dashboard'),

    path('login/', LoginViewBootstrap.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
]
