from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user-edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),

    path('roles/', views.RoleListView.as_view(), name='role-list'),
    path('roles/create/', views.RoleCreateView.as_view(), name='role-create'),
    path('roles/<int:pk>/edit/', views.RoleUpdateView.as_view(), name='role-edit'),
    path('roles/<int:pk>/delete/', views.RoleDeleteView.as_view(), name='role-delete'),

    path('permissions/', views.PermissionListView.as_view(), name='permission-list'),
    path('permissions/create/', views.PermissionCreateView.as_view(), name='permission-create'),
    path('permissions/<int:pk>/edit/', views.PermissionUpdateView.as_view(), name='permission-edit'),
    path('permissions/<int:pk>/delete/', views.PermissionDeleteView.as_view(), name='permission-delete'),
]
