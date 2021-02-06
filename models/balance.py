from behaviors.behaviors import Timestamped
from django.db import models
from django.utils.translation import gettext_lazy as _


class Balance(Timestamped):

    user = models.OneToOneField("User", verbose_name=_("user"), on_delete=models.CASCADE)
    balance = models.DecimalField(_("balance"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('balance')
        verbose_name_plural = _('balance')

    def __str__(self):
        return str(self.balance)
