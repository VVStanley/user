from .cabinet import TransactionView, DashboardView, TariffView
from .registration import (ConfirmPaswordView, LoginView, LogoutView,
                           RegisterUserView, ResetPaswordView)

__all__ = [
    # registration
    LogoutView,
    LoginView,
    ResetPaswordView,
    RegisterUserView,
    ConfirmPaswordView,

    # cabinet
    DashboardView,
    TransactionView,
    TariffView,
]
