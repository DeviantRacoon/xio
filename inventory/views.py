from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Equipment


class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = 'inventory/equipment_list.html'
    paginate_by = 20
