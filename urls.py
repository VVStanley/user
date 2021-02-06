from django.urls import path

from .views import (ConfirmPaswordView, DashboardView, LoginView, LogoutView,
                    RegisterUserView, ResetPaswordView, TransactionView, TariffView)

urlpatterns = [

    # registration
    path('register/', RegisterUserView.as_view(), name='register'),
    path('confirm/<str:confirm>/', ConfirmPaswordView.as_view(), name='confirm'),
    path('reset/', ResetPaswordView.as_view(), name='reset'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # cabinet
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('tariff/', TariffView.as_view(), name='tariff'),
]
