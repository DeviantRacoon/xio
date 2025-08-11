from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import views as auth_views

from .forms import (
    RegisterForm,
    BootstrapAuthenticationForm,
    UserForm,
    RoleForm,
    PermissionForm,
)
from .models import User, Role, Permission


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Tu cuenta fue creada correctamente. ¡Ahora puedes iniciar sesión!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class LoginViewBootstrap(auth_views.LoginView):
    authentication_form = BootstrapAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'users/users.html'
    paginate_by = 10
    permission_required = 'accounts.view_user'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('q')
        role = self.request.GET.get('role')
        if search:
            qs = qs.filter(username__icontains=search)
        if role:
            qs = qs.filter(roles__id=role)
        return qs


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('accounts:user-list')
    permission_required = 'accounts.add_user'


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('accounts:user-list')
    permission_required = 'accounts.change_user'


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user-list')
    permission_required = 'accounts.delete_user'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)


class RoleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Role
    template_name = 'roles/roles.html'
    permission_required = 'accounts.view_role'


class RoleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'roles/role_form.html'
    success_url = reverse_lazy('accounts:role-list')
    permission_required = 'accounts.add_role'


class RoleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'roles/role_form.html'
    success_url = reverse_lazy('accounts:role-list')
    permission_required = 'accounts.change_role'


class RoleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Role
    template_name = 'roles/role_confirm_delete.html'
    success_url = reverse_lazy('accounts:role-list')
    permission_required = 'accounts.delete_role'


class PermissionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Permission
    template_name = 'permissions/permissions.html'
    permission_required = 'accounts.view_permission'


class PermissionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Permission
    form_class = PermissionForm
    template_name = 'permissions/permission_form.html'
    success_url = reverse_lazy('accounts:permission-list')
    permission_required = 'accounts.add_permission'


class PermissionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Permission
    form_class = PermissionForm
    template_name = 'permissions/permission_form.html'
    success_url = reverse_lazy('accounts:permission-list')
    permission_required = 'accounts.change_permission'


class PermissionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Permission
    template_name = 'permissions/permission_confirm_delete.html'
    success_url = reverse_lazy('accounts:permission-list')
    permission_required = 'accounts.delete_permission'
