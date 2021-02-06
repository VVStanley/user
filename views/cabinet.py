from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, View
from services.models import Tariff
from users.forms import AddBalance


class DashboardView(LoginRequiredMixin, View):

    template_name = 'cabinet/dashboard.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class TransactionView(LoginRequiredMixin, View):

    template_name = 'cabinet/transaction.html'

    def get(self, request):
        context = {
            'form': AddBalance()
        }
        return render(request, self.template_name, context)


class TariffView(LoginRequiredMixin, ListView):

    template_name = 'cabinet/tariff.html'
    model = Tariff
